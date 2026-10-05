# -*- coding: utf-8 -*-
"""Sterownik wysyłki wiadomości prywatnej (PV) / 'Zapytaj o szczegóły' na Useme (Playwright).

Obsługuje nową ścieżkę komunikacji:
1. Wejście na stronę zlecenia: /pl/jobs/{job_id}/
2. Weryfikacja sesji i ewentualne odrzucenie wykluczonych autorów (własny profil)
3. Kliknięcie w przycisk 'Zapytaj o szczegóły' (lub bezpośrednia nawigacja do /pl/mesg/compose/{job_id}/{author_id}/)
4. Zamknięcie i usunięcie z DOM overlayów banera cookies
5. Wypełnienie pola 'Treść:' (textarea[name="content"] / #id_content)
6. Tryb DRY_RUN (zrzut ekranu wypełnionego formularza bez kliknięcia 'Wyślij')
7. Tryb LIVE: kliknięcie 'Wyślij wiadomość' i twarda weryfikacja wysłania.
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any, Dict, Optional

from playwright.sync_api import BrowserContext, Page

import config


class AuthenticationRequiredError(Exception):
    """Rzucany, gdy cookies wygasły i Useme wymaga logowania."""
    pass


class PVDriver:
    def __init__(self, context: BrowserContext, dry_run: bool = config.DRY_RUN):
        self.context = context
        self.dry_run = dry_run

    def _dismiss_cookie_banner(self, page: Page):
        """Usuwa banery i nakładki cookies z DOM, aby nie blokowały interakcji."""
        for sel in ["#cookiescript_accept", "button:has-text('AKCEPTUJ WSZYSTKIE')", "button:has-text('Akceptuj')"]:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible():
                    loc.click()
                    page.wait_for_timeout(300)
                    break
            except Exception:
                pass

        try:
            page.evaluate("""() => {
                document.querySelectorAll('#cookiescript_injected_wrapper, #cookiescript_wrapper, .cookie-banner, [id*="cookiescript"]').forEach(el => el.remove());
            }""")
        except Exception:
            pass

    def send_private_message(
        self,
        job_id: str,
        message_text: str,
        author_id: Optional[str] = None,
        dry_run: Optional[bool] = None,
        custom_screenshot_dir: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Wchodzi na ogłoszenie, klika 'Zapytaj o szczegóły', uzupełnia treść i wysyła (lub DRY_RUN)."""
        is_dry_run = self.dry_run if dry_run is None else dry_run
        screenshot_dir = custom_screenshot_dir or config.DEBUG_DIR
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Twardy bezpiecznik: ochrona przed wysłaniem na własny profil / wykluczonego klienta
        aid_check = str(author_id or "")
        aname_check = ""
        try:
            from storage import Storage
            job_record = Storage().load_job(job_id)
            if job_record:
                aid_check = aid_check or str(job_record.get("author_id", "") or (job_record.get("full_details") or {}).get("author_id", ""))
                aname_check = str(job_record.get("author", "") or (job_record.get("full_details") or {}).get("author", ""))
        except Exception:
            pass

        if config.is_blocked_author(aid_check, aname_check):
            raise RuntimeError(f"BLOKADA WŁASNY PROFIL: Próba kontaktu PV z wykluczonym autorem: {aname_check} ({aid_check})!")

        job_url = f"https://useme.com/pl/jobs/{job_id}/"
        page = self.context.new_page()

        try:
            print(f"[PV] Otwieram zlecenie #{job_id}: {job_url}", flush=True)
            page.goto(job_url, wait_until="domcontentloaded", timeout=config.NAV_TIMEOUT_MS)
            page.wait_for_timeout(1500)
            self._dismiss_cookie_banner(page)

            # 1. Sprawdzenie czy sesja jest aktywna
            curr_url = page.url
            if "/users/login" in curr_url or "/login" in curr_url or page.locator('input[name="login"], input[name="username"]').count() > 0:
                raise AuthenticationRequiredError(
                    f"Sesja Useme wygasła! Przekierowano do logowania: {curr_url}. Zaktualizuj tech/cookies.json."
                )

            # 2. Wyszukanie przycisku 'Zapytaj o szczegóły'
            ask_btn = page.locator('a:has-text("Zapytaj o szczegóły"), a[href*="/mesg/compose/"]').first
            compose_target_url = None

            if ask_btn.count() > 0:
                href = ask_btn.get_attribute("href") or ""
                print(f"[PV] Znaleziono przycisk 'Zapytaj o szczegóły' (href: {href})", flush=True)
                if href.startswith("/"):
                    compose_target_url = f"https://useme.com{href}"
                elif href.startswith("http"):
                    compose_target_url = href

                # Kliknięcie w przycisk
                try:
                    ask_btn.scroll_into_view_if_needed()
                    ask_btn.click(force=True)
                except Exception:
                    ask_btn.click()

                try:
                    page.wait_for_load_state("domcontentloaded", timeout=15000)
                except Exception:
                    pass
                page.wait_for_timeout(1500)
            else:
                # Fallback: jeśli znamy author_id, przechodzimy bezpośrednio
                if author_id:
                    direct_compose_url = f"https://useme.com/pl/mesg/compose/{job_id}/{author_id}/"
                    print(f"[PV] Brak przycisku na karcie zlecenia, przechodzę bezpośrednio pod: {direct_compose_url}", flush=True)
                    page.goto(direct_compose_url, wait_until="domcontentloaded", timeout=config.NAV_TIMEOUT_MS)
                    page.wait_for_timeout(1500)
                else:
                    screenshot_err = screenshot_dir / f"pv_missing_btn_{job_id}.png"
                    page.screenshot(path=str(screenshot_err), full_page=True)
                    raise RuntimeError(
                        f"Nie znaleziono przycisku 'Zapytaj o szczegóły' na {page.url} i brak podanego author_id. "
                        f"Zrzut błędu: {screenshot_err}"
                    )

            self._dismiss_cookie_banner(page)

            # 3. Weryfikacja formularza wiadomości
            curr_url = page.url
            if "/users/login" in curr_url or "/login" in curr_url:
                raise AuthenticationRequiredError(f"Przekierowano do logowania po przejściu do wiadomości: {curr_url}")

            content_textarea = page.locator('textarea[name="content"], textarea#id_content, textarea.form__textarea').first
            if content_textarea.count() == 0:
                # Może Useme przekierowało do istniejącego wątku (/pl/mesg/thread/...)
                # Sprawdzamy czy na stronie wątku jest formularz odpowiedzi
                reply_textarea = page.locator('form textarea[name="content"], #id_content').first
                if reply_textarea.count() > 0:
                    content_textarea = reply_textarea
                    print(f"[PV] Wykryto istniejący wątek konwersacji ({curr_url}). Używam pola odpowiedzi.", flush=True)
                else:
                    err_scr = screenshot_dir / f"pv_no_textarea_{job_id}.png"
                    page.screenshot(path=str(err_scr), full_page=True)
                    raise RuntimeError(f"Nie znaleziono pola textarea[name='content'] na {curr_url}. Zrzut: {err_scr}")

            content_textarea.wait_for(state="visible", timeout=10000)
            content_textarea.scroll_into_view_if_needed()

            # 4. Wpisanie treści wiadomości
            tresc = (message_text or "").strip()
            if not tresc:
                raise ValueError(f"Pusta treść wiadomości PV dla zlecenia #{job_id}!")

            # Ograniczenie Useme do 4096 znaków
            if len(tresc) > 4000:
                print(f"[PV] Ostrzeżenie: treść ma {len(tresc)} znaków (limit Useme 4096), przycinam.", flush=True)
                tresc = tresc[:4000].strip()

            content_textarea.click(force=True)
            content_textarea.fill(tresc)

            # Native setter i dispatch zdarzeń dla pewności frameworków JS
            page.evaluate("""({val}) => {
                const el = document.querySelector('textarea[name="content"]') || document.querySelector('#id_content');
                if (!el) return;
                const proto = window.HTMLTextAreaElement.prototype;
                const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
                setter.call(el, val);
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }""", {"val": tresc})

            page.wait_for_timeout(500)

            # 5. Bezpiecznik DRY_RUN
            if is_dry_run:
                proof_path = screenshot_dir / f"pv_dry_run_{job_id}.png"
                page.screenshot(path=str(proof_path), full_page=True)
                print(f"[PV DRY_RUN] Wiadomość uzupełniona. Zatrzymano przed kliknięciem 'Wyślij'. Dowód: {proof_path}", flush=True)
                return {
                    "ok": True,
                    "status": "DRY_RUN_OK",
                    "mode": "pv",
                    "job_id": str(job_id),
                    "url": page.url,
                    "dlugosc": len(tresc),
                    "tresc": tresc,
                    "proof_screenshot": str(proof_path),
                    "message": f"DRY_RUN: Treść PV dla zlecenia #{job_id} wpisana pomyślnie. Zrzut ekranu: {proof_path}"
                }

            # 6. WYSYŁKA LIVE (dry_run = False)
            submit_btn = page.locator(
                'button:has-text("Wyślij wiadomość"), button.button--primary[type="submit"], form[action*="mesg"] button[type="submit"]'
            ).first
            if submit_btn.count() == 0:
                err_btn_scr = screenshot_dir / f"pv_no_submit_btn_{job_id}.png"
                page.screenshot(path=str(err_btn_scr), full_page=True)
                raise RuntimeError(f"Nie znaleziono przycisku 'Wyślij wiadomość' na {page.url}. Zrzut: {err_btn_scr}")

            print(f"[PV LIVE] Klikam 'Wyślij wiadomość' dla zlecenia #{job_id}...", flush=True)
            self._dismiss_cookie_banner(page)

            try:
                submit_btn.click(force=True)
            except Exception:
                submit_btn.click()

            try:
                page.wait_for_load_state("domcontentloaded", timeout=15000)
            except Exception as wait_e:
                print(f"[PV] wait domcontentloaded timeout (ignorowane): {wait_e}", flush=True)

            page.wait_for_timeout(3000)

            submitted_scr = screenshot_dir / f"pv_submitted_{job_id}.png"
            page.screenshot(path=str(submitted_scr), full_page=True)
            print(f"[PV LIVE] URL po wysłaniu: {page.url}, zrzut: {submitted_scr}", flush=True)

            post_url = page.url.lower()
            post_content = page.content().lower()

            is_success = (
                "/mesg/thread/" in post_url
                or "/mesg/reply/" not in post_url and "/mesg/compose/" not in post_url
                or "wiadomość została wysłana" in post_content
                or "wysłano wiadomość" in post_content
                or page.locator('textarea[name="content"]').count() == 0
            )

            if is_success:
                return {
                    "ok": True,
                    "status": "WYSLANO_PV",
                    "mode": "pv",
                    "job_id": str(job_id),
                    "final_url": page.url,
                    "dlugosc": len(tresc),
                    "tresc": tresc,
                    "proof_screenshot": str(submitted_scr),
                    "message": f"Wiadomość PV dla zlecenia #{job_id} została pomyślnie wysłana."
                }
            else:
                raise RuntimeError(
                    f"Brak potwierdzenia wysłania PV na URL {page.url}. Zrzut błędu: {submitted_scr}"
                )

        finally:
            page.close()
