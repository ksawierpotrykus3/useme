Zacznę od rzeczy, która najczęściej rozjeżdża takie projekty. WordPress to nie miejsce, w którym voicebot ma mózg. WP hostuje tylko widget, czyli przycisk na stronie. Cały pipeline głosowy działa poza WordPressem, jako zewnętrzna usługa. Jeśli ktoś obiecuje plugin, który sam zrobi voicebota, to albo nie rozumie tematu, albo upraszcza do granicy błędu. Dlatego proponuję widget JS wklejany na stronę plus backend voice poza WP.

Do tego najkrótsza ścieżka to ElevenLabs Conversational AI z ich oficjalnym widgetem WordPress. Barge-in, przerwanie wypowiedzi i naturalny polski głos są tam dostępne od razu. Jeśli okaże się, że potrzebujesz większej kontroli nad pipeline, wtedy schodzimy do LiveKit albo Vapi, ale to już więcej pracy i wyższy koszt. Przy Twoich wymaganiach na start managed platforma wystarczy.

Kwestia latencji i przerywania. Żeby użytkownik mógł wejść w słowo, a bot natychmiast przestał mówić, potrzebny jest streaming na każdym etapie, czyli STT, LLM z RAG i TTS. Bez streamingu rozmowa brzmi sztywno i mechanicznie, bo bot czeka, aż skończysz, zamiast reagować w trakcie. VAD czyli detekcja mowy pilnuje, kiedy użytkownik zaczyna mówić.

Jedna rzecz, której w ogłoszeniu nie ma, a musi wejść do zakresu. Voicebot zbiera dane osobowe i prawdopodobnie nagrywa rozmowę. Bez klauzuli informacyjnej przed startem, zgody na nagrywanie i określonej retencji wdrożenie jest niezgodne z RODO. To nie jest straszenie, to element projektu, który po prostu trzeba dopiąć.

Koszt. 3500 do 8000 zł netto. Dla zakresu, który opisałeś, czyli voicebot na WWW z polskim głosem, barge-in, RAG i zbieraniem danych, typowy scenariusz to około 5000 do 6000 zł netto, więc mieścisz się w swoim budżecie. Dolna granica 3500 zł jest możliwa, jeśli baza wiedzy jest dobrze przygotowana i nie trzeba jej porządkować pod RAG, a WordPress jest self-hosted. Górna 8000 zł, jeśli dochodzi integracja z CRM, kalendarzem i pełne RODO. Czas to około 10 do 20 dni od momentu, gdy dostanę materiały. Koszty API ElevenLabs i LLM są po Twojej stronie, przy niewielkim ruchu to rzędu stu do trzystu złotych miesięcznie.

Co do przykładów realizacji. Nie mam case'a z branży HVAC, który mógłbym pokazać. Nie będę wstawiał cudzych realizacji ani zmyślał. Mogę natomiast opisać podejście, które stosuję w projektach voicebotowych i RAG, i ono się nie zmienia niezależnie od branży. Jeśli chcesz, na czacie pokażę Ci fragmenty architektury z podobnych wdrożeń.

Żeby zawęzić wycenę do punktu, potrzebuję trzech rzeczy. Gdzie fizycznie leży baza wiedzy firmy i w jakim jest formacie, czy to dokumenty, FAQ, arkusze, CRM. Gdzie mają trafiać dane zbierane od klienta, czy do istniejącego CRM, kalendarza, mailem, czy zapisem w WordPressie. Czy strona jest self-hosted, czy na WordPress.com i na jakim planie, bo od tego zależy, czy da się wstawić własny widget JS.

Jeśli po wdrożeniu na WWW zechcesz iść w inne kanały, to spokojnie zrobimy to jako osobny etap. Najpierw ustalmy zakres tego.

Ksawier