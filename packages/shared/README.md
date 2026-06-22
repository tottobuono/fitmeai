# packages/shared — Contratti di dominio condivisi

Tipi e modelli di dominio condivisi tra `apps/web`, `apps/api` e `workers/tryon`, per mantenere
un contratto unico e coerente attraverso il sistema.

## Contenuto previsto
- `TryOnRequest` / `TryOnResult` — contratto dell'astrazione di rendering.
- `BodyProfile` — misure e preferenze di vestibilità.
- `Garment` — capo normalizzato (immagine, categoria, size chart, brand).
- `TryOnJob` / `JobStatus` — job e relativo stato (`queued`, `processing`, `done`, `failed`).

## Note
- Solo **definizioni di tipo/contratto**: nessuna logica applicativa.
- I tipi TS qui devono restare coerenti con i modelli Pydantic lato `apps/api`.

## Stato
🚧 Placeholder. I modelli condivisi arrivano con il Task 3.
