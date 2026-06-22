"""Modelli ORM (tabelle).

Scope Fase 1: persistenza dei job di try-on. Le altre entita' di dominio (utenti,
consent record, audit, provider run) saranno aggiunte come tabelle nei layer successivi.
Si usano tipi portabili (String/JSON) per restare eseguibili anche su SQLite nei test.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TryOnJobRow(Base):
    __tablename__ = "tryon_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    mode: Mapped[str] = mapped_column(String(32), nullable=False)
    # Contratti serializzati (provider-agnostic). Nessun binario/immagine inline.
    request: Mapped[dict] = mapped_column(JSON, nullable=False)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
