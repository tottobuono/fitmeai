"""Worker async di try-on.

Consuma gli id dei job dalla coda Redis, carica il job dal DB, invoca il provider tramite
l'astrazione interna e scrive il risultato. Riusa il dominio del backend (`app.*`): il worker
e' il braccio esecutivo della stessa logica, ma resta provider-agnostic e privo di logica
di fit/sizing.

Esecuzione: vedi workers/tryon/README.md (gira nell'ambiente di apps/api).
"""

from __future__ import annotations

import asyncio
import logging
from typing import Callable

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.base import SessionLocal
from app.db.repository import TryOnJobRepository
from app.domain.enums import JobStatus
from app.queue.redis_queue import RedisJobQueue
from app.tryon import get_provider
from app.tryon.errors import ProviderQuotaError, ProviderTimeoutError, TryOnProviderError
from app.tryon.provider import VirtualTryOnProvider

logger = logging.getLogger("fitme.worker")

# Errori transitori: ha senso ritentare con backoff.
_RETRYABLE = (ProviderTimeoutError, ProviderQuotaError)

SessionFactory = Callable[[], Session]


async def process_job(
    job_id: str,
    session_factory: SessionFactory,
    provider: VirtualTryOnProvider,
    *,
    max_attempts: int = 3,
    base_backoff_s: float = 0.5,
) -> JobStatus | None:
    """Elabora un singolo job. Ritorna lo stato finale, o None se il job non esiste.

    Pura e iniettabile (session_factory + provider) per essere testata senza infra.
    """
    with session_factory() as session:
        job = TryOnJobRepository(session).get(job_id)
        if job is None:
            logger.warning("worker.job_missing id=%s", job_id)
            return None
        TryOnJobRepository(session).set_status(job_id, JobStatus.PROCESSING)

    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            result = await provider.generate(job.request)
            with session_factory() as session:
                TryOnJobRepository(session).set_result(job_id, JobStatus.DONE, result)
            logger.info(
                "worker.job_done id=%s provider=%s attempt=%d", job_id, provider.name, attempt
            )
            return JobStatus.DONE
        except _RETRYABLE as exc:
            last_error = exc
            logger.warning(
                "worker.job_retry id=%s attempt=%d reason=%s", job_id, attempt, type(exc).__name__
            )
            if attempt < max_attempts:
                await asyncio.sleep(base_backoff_s * 2 ** (attempt - 1))
        except TryOnProviderError as exc:
            last_error = exc  # errore permanente: niente retry
            break
        except Exception as exc:  # noqa: BLE001 - vogliamo marcare il job come failed
            last_error = exc
            break

    with session_factory() as session:
        TryOnJobRepository(session).set_result(
            job_id, JobStatus.FAILED, None, error=str(last_error) if last_error else "unknown"
        )
    # Log privacy-safe: solo tipo di errore, niente contenuti.
    logger.warning(
        "worker.job_failed id=%s error=%s",
        job_id,
        type(last_error).__name__ if last_error else "unknown",
    )
    return JobStatus.FAILED


def run() -> None:
    """Loop di consumo: blocca su Redis e processa i job in arrivo."""
    settings = get_settings()
    configure_logging(settings.log_level)
    queue = RedisJobQueue()
    provider = get_provider()
    logger.info("worker.start provider=%s queue=%s", provider.name, queue.queue_name)

    while True:
        job_id = queue.dequeue(timeout=5)
        if job_id is None:
            continue
        asyncio.run(process_job(job_id, SessionLocal, provider))


if __name__ == "__main__":
    run()
