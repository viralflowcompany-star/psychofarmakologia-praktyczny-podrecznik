# Manifest aktywów finalnych

- `index.html` — strona główna, język `pl-PL`.
- `styles.css` — kompletne style responsywne.
- `script.js` — karuzela, komunikat CTA i przycisk powrotu na górę.
- `images/mockup-cyfrowy-pl.png` — mockup produktu cyfrowego.
- `og.png` — karta społecznościowa oparta na mockupie.
- `package.json` / `package-lock.json` — zależności kompilacji.
- `vite.config.js` — konfiguracja Vite + Sites.
- `.openai/hosting.json` — identyfikator projektu Sites.
- `server/index.js` — minimalny worker statycznych zasobów.
- `scripts/postbuild.mjs` — umieszczenie workera w artefakcie produkcyjnym.
- `_reports/*.md` — dokumentacja audytu i QA.

Finalny build tworzy `dist/index.html`, zahashowane lokalne CSS/JS/PNG, `dist/server/index.js` i `dist/.openai/hosting.json`.
