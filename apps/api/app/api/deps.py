"""Dependency FastAPI: sessione DB e coda dei job.

Sono override-abili nei test (DB SQLite in-memory + coda fake) per non richiedere infra.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Iterator

from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.queue.base import JobQueue
from app.queue.redis_queue import RedisJobQueue


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache
def _queue_singleton() -> RedisJobQueue:
    return RedisJobQueue()


def get_queue() -> JobQueue:
    return _queue_singleton()
