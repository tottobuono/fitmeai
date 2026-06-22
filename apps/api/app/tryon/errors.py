"""Gerarchia di errori del layer di try-on.

Errori normalizzati e indipendenti dal provider: gli adapter traducono i propri
fallimenti specifici in queste classi, cosi' il codice a monte gestisce sempre lo stesso
contratto d'errore. I messaggi non devono contenere contenuti sensibili (immagini, misure).
"""

from __future__ import annotations

from typing import Optional


class TryOnProviderError(Exception):
    """Base di tutti gli errori del layer di try-on."""

    def __init__(self, message: str, *, provider: Optional[str] = None) -> None:
        super().__init__(message)
        self.provider = provider

    def __str__(self) -> str:  # pragma: no cover - banale
        base = super().__str__()
        return f"[{self.provider}] {base}" if self.provider else base


class InvalidTryOnInputError(TryOnProviderError):
    """Input non valido per il provider (es. immagine mancante o non supportata).

    Non ritentabile: ripetere la stessa richiesta fallirebbe allo stesso modo.
    """


class ProviderTimeoutError(TryOnProviderError):
    """Il provider non ha risposto entro il timeout. Tipicamente ritentabile."""


class ProviderQuotaError(TryOnProviderError):
    """Quota/rate limit del provider superati. Ritentabile con backoff."""


class UnsafeResponseError(TryOnProviderError):
    """Il provider ha segnalato/restituito un contenuto non sicuro. Non ritentabile."""


class MalformedProviderResponseError(TryOnProviderError):
    """La risposta del provider non e' interpretabile nel contratto interno."""
