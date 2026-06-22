"""Endpoint dei job di try-on.

Flusso: l'API crea il job (stato `queued`), lo persiste e ne accoda l'id. L'esecuzione
vera (chiamata al provider) avviene nel worker async (Task 6). L'API non chiama mai i
provider direttamente.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_queue
from app.api.schemas import CreateTryOnJobRequest
from app.db.repository import TryOnJobRepository
from app.domain.models import TryOnJob
from app.queue.base import JobQueue

logger = logging.getLogger("fitme.api.tryon")

router = APIRouter(prefix="/tryon-jobs", tags=["tryon"])


@router.post("", response_model=TryOnJob, status_code=status.HTTP_201_CREATED)
def create_tryon_job(
    payload: CreateTryOnJobRequest,
    db: Session = Depends(get_db),
    queue: JobQueue = Depends(get_queue),
) -> TryOnJob:
    job = TryOnJob(user_id=payload.user_id, request=payload.request)
    repo = TryOnJobRepository(db)
    created = repo.create(job)
    queue.enqueue(created.id)
    # Log privacy-safe: id e metadati, nessun URL/immagine/misura.
    logger.info("tryon_job.created id=%s mode=%s", created.id, created.request.mode.value)
    return created


@router.get("/{job_id}", response_model=TryOnJob)
def get_tryon_job(job_id: str, db: Session = Depends(get_db)) -> TryOnJob:
    job = TryOnJobRepository(db).get(job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
    return job
