"""Contratto della coda dei job.

Definito come Protocol per disaccoppiare API e worker dall'implementazione concreta
(Redis in MVP) e per consentire fake/in-memory nei test.
"""

from __future__ import annotations

from typing import Protocol


class JobQueue(Protocol):
    def enqueue(self, job_id: str) -> None:
        """Accoda l'id di un job da elaborare."""
        ...
