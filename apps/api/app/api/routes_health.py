"""Health check (liveness)."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.schemas import HealthResponse
from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", env=get_settings().env)
