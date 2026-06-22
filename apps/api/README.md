# apps/api — Backend (FastAPI)

Orchestratore centrale di Fitme.ai. Possiede i dati di dominio ed espone l'API pubblica
tipizzata (Pydantic) consumata dal frontend.

## Responsabilità
- Utenti, body profile, prodotti/capi, job di try-on, auth.
- Creazione e tracciamento dei `TryOnJob`; pubblicazione sulla coda (Redis).
- Firma degli URL di storage (S3 EU) a breve scadenza.
- Punto unico di accesso al fit/sizing engine (logica separata dai provider).

## Confini
- **Non** contiene UI.
- **Non** chiama direttamente i provider esterni: l'esecuzione dei job è delegata a `workers/tryon`.
- Mai loggare immagini, misure in chiaro o identificativi inutili.

## Struttura prevista (dai task successivi)
```
apps/api/
└── app/
    ├── main.py            # entrypoint FastAPI
    ├── api/               # router/endpoint
    ├── domain/            # modelli di dominio (Pydantic)
    ├── db/                # modelli DB + migrazioni
    ├── tryon/             # astrazione provider + factory (no fit/sizing qui)
    ├── queue/             # pubblicazione job su Redis
    └── core/              # config, logging, sicurezza
```

## Stato
🚧 Placeholder. API e modelli arrivano con i Task 3 e 5.
