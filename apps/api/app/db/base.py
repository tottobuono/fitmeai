"""Engine SQLAlchemy, factory di sessioni e Base dichiarativa.

L'engine e' creato in modo lazy (nessuna connessione all'import): import e test non
richiedono un DB raggiungibile. La sessione di richiesta e' fornita via dependency FastAPI.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


_settings = get_settings()
engine = create_engine(_settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
