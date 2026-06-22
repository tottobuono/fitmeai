"""Fixture di test: app FastAPI con DB SQLite in-memory e coda fake.

Permette di testare gli endpoint senza Postgres/Redis reali, sovrascrivendo le dependency.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db, get_queue
from app.db.base import Base
from app.main import create_app


class FakeQueue:
    def __init__(self) -> None:
        self.enqueued: list[str] = []

    def enqueue(self, job_id: str) -> None:
        self.enqueued.append(job_id)


@pytest.fixture
def queue() -> FakeQueue:
    return FakeQueue()


@pytest.fixture
def client(queue: FakeQueue) -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_queue] = lambda: queue
    return TestClient(app)


def valid_payload() -> dict:
    return {
        "user_id": "user-1",
        "request": {
            "mode": "measurements_only",
            "garment_image_url": "https://signed/garment.png",
            "avatar_image_url": "https://signed/avatar.png",
            "quality": "standard",
            "samples": 1,
            "metadata": {},
        },
    }
