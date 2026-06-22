# workers/tryon — Worker async di try-on

Consumer che esegue i job di generazione in modo asincrono, fuori dal ciclo richiesta/risposta
dell'API.

## Responsabilità
- Consumare i `TryOnJob` dalla coda (Redis).
- Invocare il provider tramite l'astrazione `VirtualTryOnProvider.generate(TryOnRequest)`.
- Salvare l'immagine risultante su storage EU e aggiornare lo stato del job (`done`/`failed`).
- Gestione base di errori e retry.

## Confini
- **Non** espone API pubbliche.
- Conosce solo il **contratto interno** del provider, non i dettagli del singolo fornitore.
- **Non** contiene logica di fit/sizing.

## Esecuzione (locale)

Il worker riusa il dominio del backend (`app.*`), quindi gira nello stesso ambiente di
`apps/api`. Con l'infrastruttura attiva (`docker compose up -d`) e le migrazioni applicate:

```bash
# usa il venv di apps/api (dove fitme-api e' installato editable)
cd apps/api && ./.venv/Scripts/python -m pip install -e ../../workers/tryon

# avvia il worker (legge REDIS_URL/DATABASE_URL/TRYON_PROVIDER da env)
cd ../../workers/tryon && "../../apps/api/.venv/Scripts/python" worker.py
```

## Logica

- `process_job(job_id, session_factory, provider)` — elabora un singolo job: lo porta a
  `processing`, invoca `provider.generate(...)`, scrive `done` con risultato o `failed` con
  errore. Pura e iniettabile (testata senza infra).
- Retry con backoff esponenziale solo per errori transitori (`ProviderTimeoutError`,
  `ProviderQuotaError`); gli altri errori sono permanenti.
- `run()` — loop di consumo: `BRPOP` su Redis, poi `process_job` per ogni id.

Test: `./.venv/Scripts/python -m pytest` (dalla cartella, con `fitme-api` nel venv).

## Stato
✅ Implementato (Task 6).
