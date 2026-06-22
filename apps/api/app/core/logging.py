"""Configurazione base del logging.

Regola di progetto (privacy by design): non loggare mai contenuti di immagini, misure in
chiaro o identificativi inutili. I logger applicativi devono passare solo metadati non
sensibili (provider, mode, status, durate). La baseline completa di privacy/logging viene
ampliata nel layer compliance.
"""

from __future__ import annotations

import logging


def configure_logging(level: str = "info") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
