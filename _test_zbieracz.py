import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from storage import Storage
from zbieracz_danych import uruchom_zbieranie
import config

def test_zbieracz():
    # Tworzymy tymczasowy katalog na magazyn
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        storage = Storage(magazyn_dir=tmp_path)
        
        # 1. Stara oferta (powinna zostać zamknięta jako PROZNIA)
        stara_data = (datetime.now() - timedelta(days=config.TIMEOUT_DNI + 2)).isoformat()
        storage.save_new_job({
            "id": "test_stary_001",
            "title": "Test Stary",
            "author_id": "author_stary",
            "category": "programowanie-i-it"
        })
        storage.update_job("test_stary_001", {
            "status": "WYSLANO",
            "data_wyslania": stara_data
        })
        
        # 2. Nowa oferta (nie powinna zostać tknięta)
        nowa_data = (datetime.now() - timedelta(days=1)).isoformat()
        storage.save_new_job({
            "id": "test_nowy_002",
            "title": "Test Nowy",
            "author_id": "author_nowy",
            "category": "programowanie-i-it"
        })
        storage.update_job("test_nowy_002", {
            "status": "WYSLANO",
            "data_wyslania": nowa_data
        })
        
        print("Przed zbieraczem:")
        print(f"Stary: {storage.load_job('test_stary_001').get('status')}")
        print(f"Nowy: {storage.load_job('test_nowy_002').get('status')}")
        
        # Uruchamiamy zbieracza (dry_run=True, żeby nie odpalał prawdziwej przeglądarki)
        uruchom_zbieranie(magazyn_dir=tmp_path, dry_run=True)
        
        # Sprawdzamy wyniki
        stary_po = storage.load_job('test_stary_001')
        nowy_po = storage.load_job('test_nowy_002')
        
        print("\nPo zbieraczu:")
        print(f"Stary: {stary_po.get('status')} (data_weryfikacji: {stary_po.get('data_weryfikacji')})")
        print(f"Nowy: {nowy_po.get('status')}")
        
        assert stary_po.get("status") == "PROZNIA", f"Oczekiwano PROZNIA, jest {stary_po.get('status')}"
        assert nowy_po.get("status") == "WYSLANO", f"Oczekiwano WYSLANO, jest {nowy_po.get('status')}"
        print("\n[SUKCES] Test zbieracza przeszedł pomyślnie!")

if __name__ == "__main__":
    test_zbieracz()