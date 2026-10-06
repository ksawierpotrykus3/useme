Zanim cokolwiek wycenię, jedna rzecz techniczna, która wpływa na wynik. APK to ZIP, ale na APKPure i APKMirror częściej dostaniesz XAPK albo APKM, czyli archiwum w archiwum, ze splitami per ABI, gęstość i język. Bez rekurencyjnego rozpakowania z fallbackiem na katalogi res/font oraz assets część fontów po prostu wypadnie i raport będzie niepełny. Proponuję pipeline pobieranie, rekurencyjny unpack, odczyt tablicy name w TTF i OTF, eksport do XLSX, a całość w panelu web z uploadem listy deweloperów i przyciskiem do raportu. Domyślnie kolumny to nazwa aplikacji, nazwa fontu, rodzina, wersja, copyright i ścieżka w APK. Jeśli pasuje, nie trzeba tego potwierdzać.

Największa niewiadoma to serwer. Przy APKPure i APKMirror kanał jest publiczny, choć niestabilny, bo leci rate limit i Cloudflare. Przy Google Play nie ma publicznego API, pobieranie zależy od konta Google, a paczki przychodzą jako split APK do scalania. To zmienia architekturę i ryzyko, więc wolę to ustalić, niż zgadywać.

Trzy pytania. Który to serwer. Ilu deweloperów i rząd wielkości aplikacji, dziesiątki czy tysiące. Jednorazowo czy cyklicznie, bo cykl to harmonogram, diff wersji i powiadomienia.

Widełki to 4500 do 12000 zł netto, około 10 do 30 dni. Dolna granica przy APKPure lub APKMirror, dziesiątkach deweloperów i prostym panelu, górna gdy wchodzi Google Play, setki aplikacji albo tryb cykliczny. Jak odpowiesz na te trzy rzeczy, podam jedną kwotę zamiast widełek i dopasuję zakres do materiału.

Ksawier