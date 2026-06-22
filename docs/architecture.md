# Fitme.ai — Architettura (high-level)

> Documento sintetico per chi arriva dopo. Si evolve insieme al codice: aggiornarlo quando
> si introducono nuovi servizi, env vars o flussi.

## 1. Vista d'insieme

```
                ┌─────────────────────────────────────────────┐
                │                 apps/web                      │
                │  Next.js + TS — onboarding, input, risultati  │
                └───────────────────────┬───────────────────────┘
                                        │ REST (tipizzata)
                                        ▼
                ┌─────────────────────────────────────────────┐
                │                 apps/api                      │
                │  FastAPI — utenti, body profile, prodotti,    │
                │  job try-on, auth, firma URL storage          │
                └───────┬──────────────────────────┬────────────┘
                        │ enqueue (Redis)           │ metadati
                        ▼                           ▼
        ┌───────────────────────────┐      ┌──────────────────┐
        │      workers/tryon         │      │   PostgreSQL      │
        │  consuma job, invoca       │      │  utenti, profili, │
        │  VirtualTryOnProvider      │      │  prodotti, job    │
        └───────────┬───────────────┘      └──────────────────┘
                    │ adapter (provider-agnostic)
                    ▼
        ┌───────────────────────────┐      ┌──────────────────┐
        │  Provider try-on esterni   │      │  Storage S3 EU    │
        │  (Mock / FASHN / Fal / …)  │      │  foto, output,    │
        └───────────────────────────┘      │  avatar (URL firm.)│
                                            └──────────────────┘
```

Frontend e worker **non** parlano mai direttamente con i provider esterni: tutto passa
dall'astrazione interna.

## 2. Servizi e confini

- **apps/web** — solo presentazione e raccolta input; comunica unicamente con `apps/api`.
- **apps/api** — orchestratore centrale: possiede dati e job, firma gli URL di storage,
  pubblica i job sulla coda. Non contiene UI né dettagli dei provider.
- **workers/tryon** — esegue i job in modo asincrono, chiama il provider tramite l'astrazione,
  salva il risultato e aggiorna lo stato del job.
- **packages/shared** — contratti di dominio condivisi (tipi), nessuna logica applicativa.

## 3. Astrazione try-on

```
VirtualTryOnProvider.generate(TryOnRequest) -> TryOnResult
```

- Adapter intercambiabili (es. `MockProvider`, `FashnProvider`, `FalProvider`).
- Selezione del provider via env var; il resto del codice conosce solo il contratto interno.
- La logica di **fit/sizing vive fuori** dagli adapter (modulo dedicato).

## 4. Flusso di un job try-on (target)

1. `web` invia misure + riferimento capo → `POST /tryon-jobs`.
2. `api` crea il `TryOnJob` (`queued`), persiste su Postgres, pubblica su Redis.
3. `worker` consuma il job, invoca `VirtualTryOnProvider.generate(...)`.
4. Il risultato (immagine) finisce su storage EU; `api`/`worker` aggiornano lo stato a `done`.
5. `web` fa polling su `GET /tryon-jobs/{id}` e mostra il risultato con etichetta **AI-generated**.

## 5. Modalità di input

- **photo+measurements** — foto utente come base per il rendering.
- **measurements-only** — avatar/modello rappresentativo scelto in base alla fascia di misure.

Stesso contratto `TryOnRequest`; cambia solo la sorgente del "body".

## 6. Privacy & compliance (trasversale)

- Foto e misure = dati personali sensibili.
- Storage in regione EU, **URL firmati a breve scadenza**, cifratura at-rest/in-transit.
- Mai loggare immagini, misure in chiaro o identificativi inutili.
- Previsti fin da subito: consenso, retention/TTL, cancellazione, export, audit.
- I provider esterni sono processor/sub-processor (DPA/SCC dove necessario).

## 7. Stato di implementazione

| Componente             | Stato        | Note                                   |
|------------------------|--------------|----------------------------------------|
| Scaffolding monorepo   | ✅ Fatto     | Task 1                                  |
| Ambiente locale        | ✅ Fatto     | Task 2 — docker-compose (pg/redis/minio)|
| Modelli di dominio     | ⬜ Da fare   | Task 3                                  |
| Astrazione + Mock      | ⬜ Da fare   | Task 4                                  |
| API job try-on         | ⬜ Da fare   | Task 5                                  |
| Worker async           | ⬜ Da fare   | Task 6                                  |
| Frontend minimale      | ⬜ Da fare   | Task 7                                  |
| Baseline privacy/log   | ⬜ Da fare   | Task 8                                  |
