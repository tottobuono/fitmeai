"""MockProvider — adapter di default per sviluppo locale e test.

Non effettua alcuna chiamata esterna e non ha costi: simula una latenza e restituisce
URL di immagini placeholder. Serve a far girare l'intera pipeline end-to-end (API -> coda
-> worker -> risultato) in Fase 1 senza dipendere da un fornitore reale.
"""

from __future__ import annotations

import asyncio
import logging
import time

from app.domain.enums import GarmentCategory, JobStatus
from app.domain.models import TryOnRequest, TryOnResult
from app.tryon.errors import InvalidTryOnInputError
from app.tryon.provider import ProviderCapabilities, VirtualTryOnProvider

logger = logging.getLogger("fitme.tryon.mock")

# Immagine placeholder neutra; nessun dato utente. In Fase 2 verra' sostituita da un
# output reale del provider salvato su storage EU e servito via URL firmato.
_PLACEHOLDER_BASE = "https://placehold.co/768x1024/png"


class MockProvider(VirtualTryOnProvider):
    """Provider fittizio deterministico."""

    name = "mock"

    def __init__(self, *, latency_s: float = 0.2) -> None:
        # Latenza simulata configurabile (0 nei test per velocita').
        self._latency_s = latency_s

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            name=self.name,
            supported_categories=list(GarmentCategory),
            max_samples=4,
            supports_async=False,
            max_resolution=1024,
        )

    async def generate(self, request: TryOnRequest) -> TryOnResult:
        # Il contratto e' gia' validato da Pydantic, ma ribadiamo l'invariante di modalita'
        # per dimostrare la traduzione errori -> eccezioni normalizzate del layer.
        if request.mode.value == "photo_measurements" and not request.person_image_url:
            raise InvalidTryOnInputError("person_image_url mancante", provider=self.name)
        if request.mode.value == "measurements_only" and not request.avatar_image_url:
            raise InvalidTryOnInputError("avatar_image_url mancante", provider=self.name)

        start = time.perf_counter()
        # Log privacy-safe: solo metadati non sensibili, nessun URL di immagini.
        logger.info(
            "tryon.generate provider=%s mode=%s samples=%d quality=%s",
            self.name,
            request.mode.value,
            request.samples,
            request.quality.value,
        )

        await asyncio.sleep(self._latency_s)

        outputs = [f"{_PLACEHOLDER_BASE}?seed={i}" for i in range(request.samples)]
        latency_ms = int((time.perf_counter() - start) * 1000)

        return TryOnResult(
            status=JobStatus.DONE,
            provider=self.name,
            output_image_urls=outputs,
            model="mock-1",
            latency_ms=latency_ms,
            cost_estimate=0.0,
            raw_response_ref=None,
        )
