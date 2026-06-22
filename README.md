# Fitme.ai

AI-native **virtual try-on** & **fit intelligence**: aiuta gli utenti a capire come un
capo visto su un e-commerce (Zara, Nike, …) starebbe sul proprio corpo, **prima** di acquistare.

Due modalità d'uso:

- **Foto + misure** → immagini fotorealistiche del capo indossato + insight di vestibilità/taglia.
- **Solo misure** → avatar/modello rappresentativo + suggerimenti di fit/taglia.

> Le immagini di try-on sono **generate da AI**, non foto reali. Questo principio è vincolante in tutta la UI.

## Struttura del monorepo

```
fitmeai/
├── apps/
│   ├── web/            # Frontend Next.js + TypeScript (onboarding, input capo, risultati)
│   └── api/            # Backend FastAPI (utenti, body profile, prodotti, job, auth, storage)
├── workers/
│   └── tryon/          # Worker async: consuma i job dalla coda e chiama i provider di try-on
├── packages/
│   └── shared/         # Tipi e contratti di dominio condivisi (TS) tra web/api/worker
├── docs/               # Documentazione high-level (architettura, setup, privacy)
└── .claude/agents/     # Prompt degli agenti specializzati
```

### Responsabilità per area

| Area              | Possiede                                                                 | Non fa                                            |
|-------------------|--------------------------------------------------------------------------|---------------------------------------------------|
| `apps/web`        | UI, onboarding, form misure/capo, visualizzazione risultati              | Non chiama mai i provider esterni direttamente    |
| `apps/api`        | Utenti, body profile, prodotti, job try-on, auth, firma URL storage      | Non contiene logica UI                             |
| `workers/tryon`   | Esecuzione async dei job, invocazione dell'astrazione provider           | Non espone API pubbliche                           |
| `packages/shared` | Modelli di dominio e contratti tipizzati condivisi                       | Nessuna logica applicativa                         |

## Principi architetturali (sintesi)

1. **Provider di try-on dietro un'unica astrazione** — `VirtualTryOnProvider.generate(TryOnRequest) -> TryOnResult`.
2. **Separazione delle responsabilità** — rendering immagine ≠ logica di fit/sizing.
3. **Provider-agnostic** — fuori dagli adapter si conosce solo il contratto interno.
4. **Semplicità prima** — niente over-engineering né microservizi prematuri.
5. **Privacy by design** — foto e misure trattate come dati personali sensibili.

Dettagli in [docs/architecture.md](docs/architecture.md).

## Stack

- **Frontend**: Next.js + TypeScript
- **Backend**: FastAPI (Python), tipizzazione forte (Pydantic)
- **Database**: PostgreSQL
- **Storage**: bucket S3-compatibile in regione EU
- **Async jobs**: Redis + worker Python
- **Virtual try-on**: adapter interno verso provider esterni (mai chiamati dal frontend)

## Stato del progetto

🚧 **Fase 1 — Fondamenta**. In corso lo scaffolding del monorepo. Le singole aree contengono
per ora solo README descrittivi; codice e configurazione arrivano con i task successivi.

Setup locale: vedi [docs/local-setup.md](docs/local-setup.md) (in arrivo con il Task 2).
