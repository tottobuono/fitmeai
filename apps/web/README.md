# apps/web — Frontend (Next.js + TypeScript)

Interfaccia utente di Fitme.ai: onboarding, raccolta misure, input del capo e
visualizzazione dei risultati di try-on.

## Responsabilità
- Onboarding e scelta modalità (**foto+misure** / **solo misure**).
- Form misure corporee e riferimento al capo (URL e-commerce o input manuale).
- Avvio job di try-on e polling dello stato.
- Visualizzazione risultati con **etichetta "Immagine generata da AI"** (obbligatoria).

## Confini
- Comunica **solo** con `apps/api` via REST.
- **Non** chiama mai i provider esterni di try-on.
- **Non** contiene logica di fit/sizing.

## Stato
🚧 Placeholder. Lo scaffolding Next.js arriverà con il Task 7.
