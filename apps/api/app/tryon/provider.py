"""Astrazione provider-agnostic per il virtual try-on.

Pattern architetturale obbligatorio:
    VirtualTryOnProvider.generate(TryOnRequest) -> TryOnResult

Ogni adapter concreto (Mock, FASHN, Fal, ...) implementa questa interfaccia e traduce
il contratto interno stabile nei parametri del fornitore. Nessuna assunzione specifica
del provider deve uscire da questo layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import GarmentCategory
from app.domain.models import TryOnRequest, TryOnResult


class ProviderCapabilities(BaseModel):
    """Capacita' dichiarate da un provider, per validazione/routing a monte."""

    model_config = ConfigDict(extra="forbid")

    name: str
    supported_categories: list[GarmentCategory]
    max_samples: int = Field(ge=1)
    supports_async: bool = False
    max_resolution: int | None = Field(default=None, ge=1, description="Lato massimo in px.")


class VirtualTryOnProvider(ABC):
    """Interfaccia interna per i provider di virtual try-on."""

    #: Identificativo stabile dell'adapter (es. "mock", "fashn"). Usato nei log/telemetria.
    name: str = "abstract"

    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        """Capacita' supportate da questo provider."""
        raise NotImplementedError

    @abstractmethod
    async def generate(self, request: TryOnRequest) -> TryOnResult:
        """Genera il try-on a partire dal contratto interno.

        Deve sollevare le eccezioni normalizzate di `app.tryon.errors` in caso di
        fallimento, e restituire un `TryOnResult` con `status=DONE` in caso di successo.
        """
        raise NotImplementedError
