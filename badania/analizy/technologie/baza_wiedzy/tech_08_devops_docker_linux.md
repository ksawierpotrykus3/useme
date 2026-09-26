# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B
## MODUŁ: DevOps, Konteneryzacja Docker, Hardening Linux, Reverse Proxy, Disaster Recovery
### Wersja: 2026.Q3 | Klasyfikacja: Wewnętrzna baza wiedzy ofertowej

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

### 1.1 Typowe zlecenia w tym bloku

| Kategoria zlecenia | Opis techniczny | Częstotliwość |
|---|---|---|
| **Konfiguracja i zabezpieczenie nowego VPS/Dedyka** | Hetzner CX/CPX, OVH Advance, AWS Lightsail/EC2 — od zera do produkcyjnego hardeningu | ~35% |
| **Migracja aplikacji do Docker Compose** | Przeniesienie legacy (PM2, systemd, bare-metal) na konteneryzację z zachowaniem stanu | ~20% |
| **Reverse proxy + SSL** | Nginx/Traefik/Caddy, Let's Encrypt (certbot/ACME), Cloudflare Tunnel | ~15% |
| **Ratowanie po infekcji malware / awarii dysku** | Forensics, odtworzenie z backupu, rotacja kluczy SSH, audyt wektorów wejścia | ~15% |
| **Automatyczne backupy off-site** | Restic/Borg + S3/B2/Hetzner Storage Box z retencją i testem restore | ~15% |

### 1.2 Budżety i profil klienta

**Widełki budżetowe:** 2 500 – 10 000 zł (mediana ~5 500 zł).

| Profil klienta | Sygnały w ogłoszeniu | Czego oczekuje |
|---|---|---|
| **Software house bez admina** | „Nie mamy DevOps, deweloperzy wdrażają ręcznie" | Powtarzalny pipeline deploy, izolacja środowisk |
| **E-commerce w szczycie** | „Pada nam strona przy 500 użytkownikach" | Limity zasobów, monitoring, stabilność pod obciążeniem |
| **Founder startupu** | „Mamy VPS, ale boję się, że coś wybuchnie" | Hardening, backupy, alerty — „święty spokój" |
| **Firma po incydencie** | „Ktoś się włamał / zaszyfrował dane" | Forensics, odtworzenie, zapobieganie nawrotom |

**Krytyczna obserwacja:** Klienci z tego bloku są **półtechniczni**. Znają pojęcia (Docker, Nginx, S3), ale nie znają **pułapek produkcyjnych**. Właśnie na tej asymetrii wiedzy buduje się przewagę ofertową.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1 Hardening Linux (Ubuntu 24.04 LTS / Debian 12)

**SSH — jedyne akceptowalne wejście administracyjne:**
- Klucze **Ed25519** (nie RSA, nie ECDSA) — `ssh-keygen -t ed25519 -a 100`. Ed25519 jest standardem złotym w 2026: odporny na side-channel, krótszy, szybszy niż RSA.
- `PermitRootLogin no`, `PasswordAuthentication no`, `PubkeyAuthentication yes`.
- Niestandardowy port (np. 2211) redukuje szum skanerów o ~95%, ale **nie jest zabezpieczeniem** — to filtr szumu.
- `AllowUsers deployuser` — whitelist kont zamiast blacklisty.

**Firewall i intrusion detection:**
- **UFW** (frontend nftables) — domyślna polityka `deny incoming`, zezwolenie tylko na 2211/tcp (SSH), 80/tcp i 443/tcp (reverse proxy). Żaden inny port publiczny nie istnieje.
- **CrowdSec** — nowoczesna alternatywa fail2ban z **bazą zagrożeń p2p**: incydent na jednym serwerze w społeczności natychmiast chroni wszystkie inne. Działa na poziomie logów aplikacyjnych i network-layer.
- **fail2ban** — nadal akceptowalny jako fallback dla starszych stacków, ale CrowdSec ma lepszą wykrywalność i mniejsze zużycie CPU na dużej liczbie incydentów.

**Automatyczne aktualizacje bezpieczeństwa:**
- `unattended-upgrades` z konfiguracją `Unattended-Upgrade::Automatic-Reboot "true"` + `Automatic-Reboot-Time "03:00"` dla kernel patches.
- **2026 reality:** brak automatycznych patchy kernel = wektor wejścia dla CVE-2024-1086 (use-after-free w netfilter, escape z kontenera do root hosta).

**SWAP / pamięć:**
- `zram` zamiast swap na dysku — kompresja w RAM, zero I/O dyskowego. Przy 4–8 GB RAM: `zram-size = ram / 2`, `vm.swappiness = 10` (agresywna ochrona przed swapem na SSD).
- **Bez zram:** OOM-killer zabija proces bazy danych przed swapem — dokładnie to, czego klient nie chce.

### 2.2 Bezpieczeństwo Docker — stan 2026

**Rootless mode — standard produkcyjny:**
- Docker daemon uruchomiony jako **użytkownik nieuprzywilejowany**, nie root. Wymaga: kernel ≥ 5.13, cgroups v2 unified hierarchy, pakiet `uidmap`.
- **User namespace remapping:** UID 0 wewnątrz kontenera → UID 100000+ na hoście. Breakout = atakujący ląduje jako `dockremap`, nie jako root systemu.
- **cgroups v2 delegation:** Bez delegacji cgroup v2 rootless Docker **nie egzekwuje limitów** `--memory` / `--cpus`. Weryfikacja: `cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/cgroup.controllers`.

**Polityka kontenerów — twarde reguły:**
- **Nigdy `USER root`** w aplikacyjnym Dockerfile. Każdy obraz: `USER 1001` lub dedykowany użytkownik z UID ≥ 1000.
- **`--read-only`** dla root filesystem + `tmpfs` dla `/tmp` i `/run`. Kontener, który nie może pisać do systemu plików, nie może trwale zainstalować backdoora.
- **`cap_drop: ALL`** + dodanie wyłącznie niezbędnych capabilities (`NET_BIND_SERVICE` jeśli aplikacja binduje port < 1024).
- **`no-new-privileges: true`** — blokada eskalacji przez setuid/setgid.

**Izolacja sieciowa — absolutny priorytet:**
- Baza danych w Docker Compose **nigdy** nie może mieć portu opublikowanego na `0.0.0.0`. Konfiguracja: sieć `internal: true` w definicji sieci bridge. Kontener bazy **nie ma** sekcji `ports:`.
- Reverse proxy komunikuje się z aplikacją przez sieć wewnętrzną. Tylko reverse proxy ma opublikowany port 443 na hoście.
- **Antywzorzec do publicznego piętnowania:** `ports: - "5432:5432"` w `docker-compose.yml` — to zaproszenie dla botnetów skanujących w ciągu 48 godzin.

**Limity zasobów — ochrona przed OOM:**
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
      pids: 100
    reservations:
      memory: 256M
```
- **Dlaczego to krytyczne:** Aplikacja Node/Python z memory leakiem zjada cały RAM hosta. Jądro Linuksa uruchamia OOM-killera, który zabija **proces bazy danych** — nie aplikację. Utrata transakcji, możliwa korupcja tabel.

**Logi Dockera — cichy zabójca dysku:**
- Domyślny sterownik `json-file` **nie ma limitu rozmiaru**. Po 2 miesiącach logi kontenera (szczególnie Node.js z `console.log` w pętli) zapychają 100% inode lub storage.
- **Wymóg:** `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "50m", "max-file": "3" }
}
```
- Efekt: maksymalnie 150 MB logów na kontener zamiast niekontrolowanego wzrostu.

### 2.3 Reverse Proxy — wybór i konfiguracja 2026

| Proxy | Throughput HTTP/1.1 | Throughput HTTP/2 | TLS 1.3 | Auto-TLS | Docker-native | Kiedy wybrać |
|---|---|---|---|---|---|---|
| **Nginx** | ~72k req/s | ~85k req/s | ✅ | ❌ (certbot) | ❌ | Max wydajność statyczna, zespół zna Nginx |
| **Traefik** | ~42.5k req/s | ~19.6k req/s | ✅ | ✅ (ACME) | ✅ (Docker provider) | Środowisko Docker-heavy, dynamiczne service discovery |
| **Caddy** | ~34.6k req/s | ~31.3k req/s | ✅ | ✅ (ACME natywnie) | ✅ | Najprostsza konfiguracja, auto-HTTPS out-of-the-box |

**Twarde wymagania dla każdego proxy:**
- **TLS 1.3 wymuszony**, TLS 1.2 akceptowany tylko dla legacy klientów. `ssl_protocols TLSv1.3;` lub `tls { protocols tls1.3 }`.
- **HSTS:** `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.
- **Nagłówki bezpieczeństwa:** `X-Frame-Options: DENY`, `X- „Potrzebuję skonfigurować serwer VPS pod naszą aplikację w Dockerze i podpiąć domenę."

**Co go utopi:**
Domyślny sterownik logów `json-file` w Dockerze **nie ma limitu rozmiaru**. Aplikacja Node.js z biblioteką `winston` lub Python z `logging` w trybie DEBUG generuje setki MB logów dziennie. Po 6–8 tygodniach:

1. Logi kontenera aplikacji zapychają partycję `/var/lib/docker` do 100%.
2. Docker przestaje pisać — kontener aplikacji crashuje.
3. Baza danych (Postgres/MySQL) w tym samym wolumenie Docker **również crashuje** — nie może zapisać WAL / binlog.
4. Przy nagłym zatrzymaniu Postgresa z niepełnym WAL → **uszkodzenie tabel** wymagające `pg_resetwal` (utrata transakcji).

**Rozwiązanie w ofercie:**
- Konfiguracja `/etc/docker/daemon.json` z `log-opts: { max-size: "50m", max-file: "3" }`.
- Monitoring rozmiaru partycji `/var/lib/docker` z alertem przy 80%.
- Rotacja logów aplikacyjnych na poziomie aplikacji (nie tylko Docker).

### MINA 2: OOM Killer zabija bazę danych

**Klient pisze:**
> „Aplikacja czasem się zawiesza, ale restart pomaga."

**Co go utopi:**
Aplikacja Node/Python ma wyciek pamięci. Po 12–48 godzinach zużywa cały RAM hosta. Jądro Linuksa uruchamia **OOM-killer**, który zabija proces o najwyższym zużyciu pamięci — **nie aplikację, a bazę danych** (Postgres/MySQL mają wyższy `oom_score_adj` niż procesy użytkownika w niektórych konfiguracjach).

**Skutek:** Nagłe zabicie Postgresa w trakcie transakcji → uszkodzenie indeksów, utrata niezacommitowanych transakcji, konieczność odtworzenia z backupu (jeśli istnieje).

**Rozwiązanie w ofercie:**
- Twarde limity `deploy.resources.limits.memory` dla **każdego** kontenera.
- `pids: 100` — ochrona przed fork-bomb.
- Monitoring zużycia RAM z alertem przy 75% — **zanim** OOM-killer zostanie uruchomiony.
- `zram` jako bufor przed OOM — kompresja pamięci zamiast natychmiastowego kill.

### MINA 3: Baza otwarta na świat (0.0.0.0:5432)

**Klient pisze:**
> „Skonfiguruj mi Postgresa w Dockerze, żebym mógł się łączyć z DataGripem z laptopa."

**Co go utopi:**
```yaml
# TO JEST WYCZEK
ports:
  - "5432:5432"
```
Port bazy opublikowany na `0.0.0.0` = **każdy botnet na świecie** może próbować się połączyć. Skanery (Shodan, Censys, botnety Mirai) skanują cały IPv4 w ciągu **godzin**. Domyślne hasło `postgres` / `admin` / puste — przejęcie bazy w ciągu **48 godzin**. Żądanie okupu w Bitcoinach.

**Rozwiązanie w ofercie:**
- Sieć `internal: true` dla bazy — **zero ekspozycji na interfejs publiczny**.
- Dostęp do bazy wyłącznie przez SSH tunnel (`ssh -L 5432:localhost:5432 deployuser@vps`) lub VPN (WireGuard/Tailscale).
- **Nigdy** `ports:` w sekcji bazy danych. Tylko `expose:` (widoczność w sieci wewnętrznej Dockera).

### MINA 4: Backup przez `cp -r` / `rsync` na żywej bazie

**Klient pisze:**
> „Mamy skrypt, który kopiuje `/var/lib/docker/volumes/postgres_data` na drugi dysk."

**Co go utopi:**
Kopiowanie plików silnika bazy danych (`PGDATA`, `ibdata1`) **podczas pracy** bazy = gwarantowane uszkodzenie spójności transakcyjnej. Baza w trakcie zapisu ma niekompletny WAL / binlog. Odtworzenie z takiej kopii = baza w stanie „crash recovery" lub całkowicie nienadająca się do uruchomienia.

**Rozwiązanie w ofercie:**
- `pg_dump -Fc` / `mysqldump --single-transaction` — logiczny backup ze spójnością transakcyjną.
- Lub snapshot LVM / ZFS ze snapshotem **po** `pg_start_backup()` / **przed** `pg_stop_backup()`.
- Lub `wal-g` / `pgBackRest` dla PITR (Point-in-Time Recovery).
- **Zasada:** backup bazy danych to **logiczny dump**, nie kopia plików.

---

## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ OFERTY

### Wariant A — uniwersalny (dla większości zleceń)

> „Zanim dotkniemy reverse proxy, sprawdzam **czy baza danych ma jakikolwiek port opublikowany na 0.0.0.0** — to najczęstszy wektor przejęcia w 48h. Drugi priorytet to **limity logów Dockera** (`max-size: "50m"`), bo domyślny `json-file` bez limitu zapycha dysk w 6–8 tygodni i crashuje bazę."

### Wariant B — dla zleceń „migracja do Docker"

> „Migracja na Docker Compose bez **izolowanej sieci `internal: true` dla bazy** i **limitów OOM** to przeniesienie tych samych problemów z bare-metal na kontenery — z bonusem w postaci szybszego zapychania dysku przez logi. Zaczynam od `daemon.json` z log-opts i limitami, dopiero potem piszę compose."

### Wariant C — dla zleceń „backup / disaster recovery"

> „Kopia zapasowa, która nie została **przetestowana procedurą odtworzenia (test restore)**, nie istnieje — to nie backup, to placebo. Druga rzecz: `cp -r` na żywym PGDATA to nie backup, to **gwarantowane uszkodzenie spójności transakcyjnej**. Wdrażam Restic do S3 z Object Lock i **automatycznym testem restore** na staging."

### Wariant D — dla zleceń „serwer po infekcji"

> „Pierwsze 15 minut to **nie** czyszczenie malware — to **odcięcie sieci** i pobranie snapshotu dysku do forensics. Drugie 15 minut: weryfikacja, czy backupy **nie zostały zaszyfrowane razem z danymi produkcyjnymi** (jeśli były na tym samym koncie S3 bez Object Lock — są bezużyteczne)."

---

## 5. CZERWONA LISTA / ANTYWZORCE — CZEGO KATEGORYCZNIE NIE PISAĆ

| Antywzorzec | Dlaczego to zabija ofertę | Co pisać zamiast tego |
|---|---|---|
| `ports: - "5432:5432"` w Docker Compose | Natychmiastowa dyskwalifikacja w oczach CTO — to publiczne zaproszenie do przejęcia bazy | „Sieć `internal: true`, dostęp wyłącznie przez SSH tunnel / VPN" |
| `USER root` w Dockerfile | Junior nie wie, że kontener root = root na hoście przy breakout | „`USER 1001`, `cap_drop: ALL`, `--read-only`" |
| `cp -r /var/lib/docker/volumes/...` jako backup | Gwarantowane uszkodzenie spójności transakcyjnej bazy | „`pg_dump -Fc` / `mysqldump --single-transaction` lub snapshot LVM" |
| „Skonfiguruję Nginx i certbot" bez wzmianki o TLS 1.3 i HSTS | Klient techniczny wie, że TLS 1.2 to już nie standard w 2026 | „TLS 1.3 wymuszony, HSTS preload, CSP, X-Frame-Options" |
| „Zrobię backup na S3" bez Object Lock | Backup na S3 bez WORM = ransomware szyfruje również backup | „S3 Object Lock w Compliance mode, 3-2-1-1-0" |
| „Użyję fail2ban" bez wzmianki o CrowdSec | W 2026 fail2ban to legacy — klient techniczny to wyłapie | „CrowdSec z bazą p2p — incydent na jednym serwerze chroni wszystkie" |
| „Spotkajmy się na Google Meet" | **Zakaz komunikacji werbalnej** — Useme to platforma pisemna | „Odpowiem na priv w ciągu 2h, komunikacja wyłącznie pisemna" |
| „Mam 5 lat doświadczenia w DevOps" | Marketingowe lanie wody — klient techniczny to wyczuje | Otwarcie problemem architektonicznym, nie CV |

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE

### 6.1 Docelowa architektura referencyjna (single-node VPS)

```
┌─────────────────────────────────────────────────────────────┐
│                        HOST (Ubuntu 24.04)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              nftables / UFW (deny incoming)           │   │
│  │         Porty publiczne: 2211/tcp, 80/tcp, 443/tcp    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         CrowdSec (p2p threat intelligence)            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Docker daemon (rootless / userns-remap)           │   │
│  │     daemon.json: log-opts max-size 50m, max-file 3    │   │
│  │     cgroups v2: delegacja dla limitów --memory/--cpus │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Sieć bridge: frontend (external)                     │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │  Reverse Proxy (Nginx/Traefik/Caddy)          │    │   │
│  │  │  TLS 1.3, HSTS, CSP, ACME (Let's Encrypt)    │    │   │
│  │  │  Porty: 80:80, 443:443                        │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Sieć bridge: backend (internal: true)                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │   │
│  │  │  Aplikacja   │  │  Aplikacja   │  │   Baza    │  │   │
│  │  │  (Node/PHP)  │  │  (Worker)    │  │ (Postgres)│  │   │
│  │  │  USER 1001   │  │  USER 1001   │  │ USER 999  │  │   │
│  │  │  mem: 512M   │  │  mem: 256M   │  │ mem: 1G   │  │   │
│  │  │  cpus: 1.0   │  │  cpus: 0.5   │  │ cpus: 2.0 │  │   │
│  │  └──────────────┘  └──────────────┘  └───────────┘  │   │
│  │  Baza NIE MA portu na hoście — tylko expose: 5432     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Restic / BorgBackup (systemd timer, co 6h)          │   │
│  │  → pg_dump (spójność) → deduplikacja → szyfrowanie    │   │
│  │  → S3 (Hetzner/B2) z Object Lock (Compliance mode)   │   │
│  │  → test restore na staging co tydzień                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Monitoring: Node Exporter + Uptime Kuma              │   │
│  │  Alerty: Telegram/Discord (dysk > 80%, RAM > 75%,    │   │
│  │  backup fail, cert expiry < 14 dni)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Rozbicie modułowe wyceny (4 000 – 9 000 zł)

| # | Moduł | Zakres | Czas | Wycena (zł) |
|---|---|---|---|---|
| **1** | **Audyt i hardening bazowy Linux** | SSH Ed25519, UFW/nftables, CrowdSec, unattended-upgrades, zram, `sysctl` hardening, audit sesji | 4–6h | 1 000 – 1 500 |
| **2** | **Środowisko Docker z polityką bezpieczeństwa** | `daemon.json` (log-opts, userns-remap), rootless mode, izolowane sieci bridge, limity `deploy.resources`, `USER 1001` w Dockerfile | 4–6h | 1 200 – 1 800 |
| **3** | **Reverse proxy + routing SSL/TLS** | Wybór proxy, konfiguracja TLS 1.3, HSTS, CSP, X-Frame-Options, ACME (Let's Encrypt / Cloudflare), Traefik + socket-proxy | 4–5h | 1 000 – 1 500 |
| **4** | **Pipeline backupów 3-2-1-1-0** | Restic/Borg, `pg_dump` ze spójnością, deduplikacja, szyfrowanie, S3 z Object Lock, retencja, automatyczny test restore | 6–8h | 1 500 – 2 500 |
| **5** | **Monitoring i alerty** | Node Exporter, Uptime Kuma (lub Grafana Cloud), alerty Telegram/Discord, monitoring certyfikatów, dysku, RAM | 3–4h | 800 – 1 200 |
| **6** | **Dokumentacja i handover** | Runbook: procedury restore, rotacja kluczy, skalowanie, troubleshooting | 2–3h | 500 – 800 |
| | **RAZEM** | | **23–32h** | **4 000 – 9 000** |

**Strategia ofertowa:** Moduły 1–3 jako **pakiet bazowy** (hardening + Docker + SSL). Moduły 4–5 jako **pakiet ciągłości** (backup + monitoring). Moduł 6 **zawsze w cenie** — runbook to dowód profesjonalizmu.

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK OFERTY)

Pytania są zaprojektowane tak, aby:
1. **Wymusić odpowiedź na priv** — klient musi odpisać, żeby dostać wycenę.
2. **Ujawnić dojrzałość infrastruktury** — odpowiedź mówi więcej niż całe ogłoszenie.
3. **Położyć fundament pod modułową wycenę** — każde pytanie mapuje się na konkretny moduł.

### Pytanie 1 — architektura bazy i sieci
> **Czy baza danych działa na tym samym hoście co aplikacja (single-node) i czy jest już w Dockerze, czy na bare-metal? Jeśli w Dockerze — czy jej port jest publikowany na `0.0.0.0`, czy wyłącznie w sieci wewnętrznej?**

*Mapowanie:* odpowiedź determinuje, czy moduł 2 wymaga **rekonfiguracji sieci** (usunięcie `ports:` z bazy), czy tylko hardeningu istniejącej konfiguracji. Jeśli baza jest na bare-metal — dodatkowy czas na migrację lub konfigurację `pg_hba.conf` z dostępem tylko z sieci Dockera.

### Pytanie 2 — wolumen danych i RTO/RPO
> **Jaki jest obecny wolumen danych produkcyjnych (rozmiar bazy + uploadów) i jaki jest akceptowalny **RTO** (czas odtworzenia po awarii) oraz **RPO** (maksymalna utrata danych w minutach/godzinach)?**

*Mapowanie:* RPO < 15 min = wymagany **PITR** (wal-g / pgBackRest), nie tylko `pg_dump`. RTO < 1h = wymagany **hot standby** lub szybki restore z snapshotu. To bezpośrednio wpływa na moduł 4 — z `pg_dump` co 6h robi się architektura z continuous archiving.

### Pytanie 3 — obecny stan i wektor wejścia
> **Czy serwer był już skanowany przez CrowdSec/Lynis, czy w ostatnich 6 miesiącach były nieudane próby logowania SSH lub nietypowe procesy? Czy backupy już istnieją — a jeśli tak, czy był wykonywany test restore?**

*Mapowanie:* Jeśli były incydenty — moduł 1 wymaga **forensics** (AIDE, ClamAV, analiza logów) przed hardeningiem. Jeśli backupy istnieją, ale bez testu restore — **nie istnieją** z punktu widzenia ciągłości działania. To argument za modułem 4.

---

## ZAŁĄCZNIK A: SZYBKIE KOMMENDY WERYFIKACYJNE DLA OFERTY

```bash
# Weryfikacja cgroups v2 (wymóg rootless Docker + limity)
cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/cgroup.controllers
# Oczekiwane: memory pids cpu (bez tego limity nie działają)

# Weryfikacja czy baza nie jest wystawiona publicznie
docker ps --format '{{.Names}}\t{{.Ports}}' | grep -E '5432|3306'
# Jeśli widzisz 0.0.0.0:5432 -> CZERWONA FLAGA

# Weryfikacja limitu logów Dockera
cat /etc/docker/daemon.json | jq '.log-opts'
# Oczekiwane: {"max-size": "50m", "max-file": "3"}

# Weryfikacja rozmiaru partycji Docker
df -h /var/lib/docker
# Jeśli >80% -> ryzyko zapchania logami

# Weryfikacja wersji OpenSSH i algorytmów
ssh -Q key | grep ed25519
sshd -T | grep -E 'permitrootlogin|passwordauth'
```

## ZAŁĄCZNIK B: FRAZY OTWIERAJĄCE OFERTĘ — WZORCE DO WYKORZYSTANIA

1. **„Zanim dotkniemy reverse proxy, sprawdzam czy baza nie ma portu na 0.0.0.0 — to wektor przejęcia w 48h."**
2. **„Domyślny json-file w Dockerze nie ma limitu — logi zapychają dysk i crashują bazę w 6–8 tygodni."**
3. **„Kopia bez testu restore nie istnieje — to placebo, nie backup."**
4. **„`cp -r` na żywym PGDATA to nie backup, to gwarantowane uszkodzenie spójności transakcyjnej."**
5. **„Rootless Docker + cgroups v2 to w 2026 nie opcja, to baseline bezpieczeństwa."**
6. **„S3 bez Object Lock = ransomware szyfruje również twoje backupy."**
7. **„Wycena rozbita na moduły — nie ryczałt. Płacisz za architekturę, nie za godziny."**

---

*Karta wiedzy zatwierdzona do użytku wewnętrznego. Aktualizacja kwartalna — następny przegląd: 2026.Q4.*