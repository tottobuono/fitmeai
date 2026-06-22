"""Layer di virtual try-on: astrazione provider-agnostic e adapter.

Nessun codice fuori da questo package deve conoscere i dettagli di un singolo provider:
si dipende solo dal contratto `VirtualTryOnProvider.generate(TryOnRequest) -> TryOnResult`.
La logica di fit/sizing NON vive qui.
"""

from app.tryon.errors import (
    InvalidTryOnInputError,
    MalformedProviderResponseError,
    ProviderQuotaError,
    ProviderTimeoutError,
    TryOnProviderError,
    UnsafeResponseError,
)
from app.tryon.factory import get_provider
from app.tryon.provider import ProviderCapabilities, VirtualTryOnProvider

__all__ = [
    "VirtualTryOnProvider",
    "ProviderCapabilities",
    "get_provider",
    "TryOnProviderError",
    "InvalidTryOnInputError",
    "ProviderTimeoutError",
    "ProviderQuotaError",
    "UnsafeResponseError",
    "MalformedProviderResponseError",
]
