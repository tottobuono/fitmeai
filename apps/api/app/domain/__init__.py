"""Modelli di dominio condivisi (contratti) di Fitme.ai.

Questi modelli definiscono i contratti che attraversano i confini del sistema
(API <-> worker <-> frontend). Devono restare coerenti con i tipi TypeScript in
`packages/shared`. Sono contratti di dominio, non lo schema di persistenza completo
(le entita' DB come ConsentRecord/AuditEvent/ProviderRun arrivano col layer di persistenza).
"""

from app.domain.enums import (
    FitPreference,
    GarmentCategory,
    JobStatus,
    MeasurementUnit,
    TryOnMode,
    TryOnQuality,
)
from app.domain.models import (
    BodyMeasurements,
    BodyProfile,
    Garment,
    TryOnJob,
    TryOnRequest,
    TryOnResult,
)

__all__ = [
    "FitPreference",
    "GarmentCategory",
    "JobStatus",
    "MeasurementUnit",
    "TryOnMode",
    "TryOnQuality",
    "BodyMeasurements",
    "BodyProfile",
    "Garment",
    "TryOnJob",
    "TryOnRequest",
    "TryOnResult",
]
