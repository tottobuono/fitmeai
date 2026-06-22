# Fitme.ai — Setup ambiente locale

Guida per avviare l'infrastruttura di sviluppo in locale. In questa fase (Fase 1) il
`docker-compose` avvia **solo i servizi di base**: PostgreSQL, Redis e MinIO (storage
S3-compatibile). I servizi applicativi (`apps/api`, `workers/tryon`, `apps/web`) si
eseguono per ora a parte e verranno aggiunti al compose quando avranno un Dockerfile.

## Prerequisiti
- Docker + Docker Compose v2 (`docker compose`, non `docker-compose`).
- Porte libere: `5432` (Postgres), `6379` (Redis), `9000` / `9001` (MinIO).

## 1. Configurare le variabili d'ambiente
```bash
cp .env.example .env
```
Adatta i valori se necessario. **Non** committare `.env` (è in `.gitignore`).

## 2. Avviare l'infrastruttura
```bash
docker compose up -d
```
Questo avvia Postgres, Redis, MinIO e un job one-shot (`minio-init`) che crea il bucket
`STORAGE_BUCKET` se non esiste.

Verifica lo stato:
```bash
docker compose ps
```

## 3. Endpoint locali

| Servizio        | URL / connessione                               | Note                              |
|-----------------|-------------------------------------------------|-----------------------------------|
| PostgreSQL      | `postgresql://fitme:***@localhost:5432/fitme`   | credenziali da `.env`             |
| Redis           | `redis://localhost:6379/0`                      | coda job async                    |
| MinIO (S3 API)  | `http://localhost:9000`                         | usato dal backend per gli asset   |
| MinIO (console) | `http://localhost:9001`                         | login con `STORAGE_ACCESS_KEY/SECRET_KEY` |

## 4. Comandi utili
```bash
docker compose logs -f postgres   # log di un servizio
docker compose down               # ferma i servizi (mantiene i volumi/dati)
docker compose down -v            # ferma e CANCELLA i dati (reset pulito)
```

## Note privacy / compliance
- MinIO emula localmente uno storage S3 in regione EU (`STORAGE_REGION=eu-central-1`).
- Gli asset (foto, output) non devono uscire dal sistema in chiaro: l'accesso avverrà via
  **URL firmati a breve scadenza** (`STORAGE_SIGNED_URL_TTL`), implementati lato `apps/api`.
- I volumi locali (`postgres_data`, `redis_data`, `minio_data`) possono contenere dati
  personali: trattali come tali e usa `down -v` per ripulirli quando servono reset.

## Prossimi passi
- **Task 3** — modelli di dominio condivisi (`packages/shared`, `apps/api/.../domain`).
- **Task 5/6/7** — quando `api`, `worker` e `web` avranno un Dockerfile, verranno aggiunti
  a `docker-compose.yml` come servizi dedicati.
