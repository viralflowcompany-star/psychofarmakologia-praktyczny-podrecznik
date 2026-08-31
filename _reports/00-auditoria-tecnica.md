# Audyt techniczny projektu źródłowego

- `PROJECT_ROOT`: `E:\downloads\Psicofarmacos`
- `PROJECT_NAME`: strona sprzedażowa podręcznika „Prescrição em Psiquiatria — Psicofármacos”
- `OUTPUT_ROOT`: `E:\downloads\Psicofarmacos-PL`
- Typ: statyczny eksport WordPress / Astra / Elementor, jedna trasa (`index.html`).
- Projekt źródłowy: 262 pliki, 27 487 243 bajty; 18 CSS, 17 JS, 107 obrazów i 119 fontów.
- Wszystkie 761 lokalnych odwołań w eksporcie wskazywały na istniejące pliki.

## Problemy wykryte

- 6 zewnętrznych CTA Eduzz, w tym 3 dla wersji fizycznej.
- VSL VTurb/ConverteAí i skrypt zdalnego playera.
- GTM, GA4, Meta Pixel, Stape/server-side tracking i powielone kontenery śledzące.
- 31 wystąpień zewnętrznych adresów HTTP(S), obejmujących 23 rzeczywiste zasoby/endpointy po pominięciu przestrzeni nazw SVG.
- Powiązania z domeną `interpretarexames.com`, WordPress REST, oEmbed, XML-RPC i stare metadane.
- Treści brazylijskie: BRL, raty, CNPJ, wysyłka, dostawa, produkt fizyczny i nazwy poprzedniego właściciela.
- 9 nieprawidłowo zapisanych atrybutów `data-settings` i fragment DOM skopiowany z interfejsu ChatGPT.

## Decyzja wdrożeniowa

Zachowano kolejność i charakter sekcji sprzedażowych, ale kod wynikowy odtworzono jako lekką stronę statyczną. Pozwoliło to usunąć kod właściciela, tracking, checkout, zależności WordPress/Elementor i zdalne warunki wykonania bez przenoszenia martwego lub ryzykownego kodu.
