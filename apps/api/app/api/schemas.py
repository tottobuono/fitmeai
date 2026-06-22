"""Schemi I/O dell'API HTTP.

Riusano i contratti di dominio (`TryOnRequest`, `TryOnJob`) per evitare divergenze.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.domain.models import TryOnRequest


class CreateTryOnJobRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # In Fase 1 l'utente e' un identificativo opaco; l'auth reale arriva in Fase 2.
    user_id: str = Field(min_length=1, max_length=64)
    request: TryOnRequest


class HealthResponse(BaseModel):
    status: str
    env: str
