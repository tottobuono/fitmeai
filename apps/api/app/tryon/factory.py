"""Factory/registry per la selezione del provider di try-on.

La selezione avviene via env var `TRYON_PROVIDER` (default: "mock"). Aggiungere un nuovo
provider in futuro = registrarlo qui, senza toccare il codice a monte.
"""

from __future__ import annotations

import os
from typing import Callable

from app.tryon.errors import TryOnProviderError
from app.tryon.provider import VirtualTryOnProvider
from app.tryon.providers.mock import MockProvider

# Registro nome -> costruttore. I provider reali (FASHN/Fal) verranno aggiunti in Fase 2,
# leggendo le proprie chiavi esclusivamente da env/secrets dentro il rispettivo adapter.
_REGISTRY: dict[str, Callable[[], VirtualTryOnProvider]] = {
    "mock": MockProvider,
}

DEFAULT_PROVIDER = "mock"


def available_providers() -> list[str]:
    """Nomi dei provider registrati."""
    return sorted(_REGISTRY)


def get_provider(name: str | None = None) -> VirtualTryOnProvider:
    """Restituisce un'istanza del provider richiesto.

    Se `name` e' None, usa l'env var `TRYON_PROVIDER` (fallback: "mock").
    Solleva `TryOnProviderError` se il provider non e' registrato.
    """
    resolved = (name or os.getenv("TRYON_PROVIDER") or DEFAULT_PROVIDER).strip().lower()
    factory = _REGISTRY.get(resolved)
    if factory is None:
        raise TryOnProviderError(
            f"Provider '{resolved}' non registrato. Disponibili: {available_providers()}"
        )
    return factory()
