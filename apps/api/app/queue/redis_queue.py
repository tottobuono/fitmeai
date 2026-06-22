"""Implementazione Redis della coda dei job.

Coda semplice basata su list: l'API fa LPUSH dell'id job, il worker fa BRPOP (Task 6).
Si accoda solo l'id (nessun dato sensibile transita nella coda); il payload completo
vive nel DB.
"""

from __future__ import annotations

import redis

from app.core.config import get_settings


class RedisJobQueue:
    def __init__(self, url: str | None = None, queue_name: str | None = None) -> None:
        settings = get_settings()
        self._client = redis.Redis.from_url(url or settings.redis_url)
        self._queue_name = queue_name or settings.redis_queue_name

    @property
    def queue_name(self) -> str:
        return self._queue_name

    def enqueue(self, job_id: str) -> None:
        self._client.lpush(self._queue_name, job_id)

    def dequeue(self, timeout: int = 5) -> str | None:
        """Estrae bloccante (usato dal worker). Ritorna l'id o None allo scadere del timeout."""
        item = self._client.brpop([self._queue_name], timeout=timeout)
        if item is None:
            return None
        _, value = item
        return value.decode() if isinstance(value, bytes) else str(value)
