"""Repository per i job di try-on: traduce tra modelli di dominio e righe ORM.

Tiene separati i contratti di dominio (Pydantic) dalla rappresentazione di persistenza.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.domain.enums import JobStatus
from app.domain.models import TryOnJob, TryOnRequest, TryOnResult
from app.db.models import TryOnJobRow


def _to_domain(row: TryOnJobRow) -> TryOnJob:
    return TryOnJob(
        id=row.id,
        user_id=row.user_id,
        status=JobStatus(row.status),
        request=TryOnRequest(**row.request),
        result=TryOnResult(**row.result) if row.result else None,
        error=row.error,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class TryOnJobRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, job: TryOnJob) -> TryOnJob:
        row = TryOnJobRow(
            id=job.id,
            user_id=job.user_id,
            status=job.status.value,
            mode=job.request.mode.value,
            request=job.request.model_dump(mode="json"),
            result=job.result.model_dump(mode="json") if job.result else None,
            error=job.error,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        self._session.add(row)
        self._session.commit()
        return _to_domain(row)

    def get(self, job_id: str) -> TryOnJob | None:
        row = self._session.get(TryOnJobRow, job_id)
        return _to_domain(row) if row else None

    def set_status(self, job_id: str, status: JobStatus) -> TryOnJob | None:
        """Aggiorna solo lo stato del job (es. queued -> processing)."""
        row = self._session.get(TryOnJobRow, job_id)
        if row is None:
            return None
        row.status = status.value
        row.updated_at = datetime.now(timezone.utc)
        self._session.commit()
        return _to_domain(row)

    def set_result(self, job_id: str, status: JobStatus, result: TryOnResult | None,
                   error: str | None = None) -> TryOnJob | None:
        """Aggiorna stato/risultato di un job (usato dal worker in Task 6)."""
        row = self._session.get(TryOnJobRow, job_id)
        if row is None:
            return None
        row.status = status.value
        row.result = result.model_dump(mode="json") if result else None
        row.error = error
        row.updated_at = datetime.now(timezone.utc)
        self._session.commit()
        return _to_domain(row)
