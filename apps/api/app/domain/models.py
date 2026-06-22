"""Modelli di dominio (Pydantic v2) — contratti condivisi di Fitme.ai.

Principi:
- Provider-agnostic: `TryOnRequest`/`TryOnResult` non contengono dettagli di alcun fornitore.
- Separazione: nessuna logica di fit/sizing qui dentro (vive nel fit engine dedicato).
- Privacy by design: le immagini sono referenziate via URL firmati / chiavi di storage,
  mai come binari; questi campi non vanno mai loggati in chiaro.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import (
    FitPreference,
    GarmentCategory,
    JobStatus,
    MeasurementUnit,
    TryOnMode,
    TryOnQuality,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid4())


class DomainModel(BaseModel):
    """Base comune: vieta campi extra per mantenere il contratto stretto."""

    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------- #
# Body
# --------------------------------------------------------------------------- #
class BodyMeasurements(DomainModel):
    """Misure corporee canoniche.

    Valori sempre in unita' metriche (cm / kg) come rappresentazione interna;
    `unit` indica come l'utente le ha inserite per eventuale conversione in UI.
    Le misure sono dati personali sensibili: da non loggare in chiaro.
    """

    height_cm: float = Field(gt=0, le=260, description="Altezza in cm")
    weight_kg: float = Field(gt=0, le=400, description="Peso in kg")
    chest_cm: Optional[float] = Field(default=None, gt=0, le=250, description="Circonferenza torace")
    waist_cm: Optional[float] = Field(default=None, gt=0, le=250, description="Circonferenza vita")
    hips_cm: Optional[float] = Field(default=None, gt=0, le=250, description="Circonferenza fianchi")
    inseam_cm: Optional[float] = Field(default=None, gt=0, le=150, description="Cavallo/lunghezza interno gamba")
    unit: MeasurementUnit = Field(default=MeasurementUnit.METRIC)
    fit_preference: FitPreference = Field(default=FitPreference.REGULAR)


class BodyProfile(DomainModel):
    """Profilo corporeo di un utente.

    Le eventuali foto NON sono incluse qui: sono referenziate tramite chiavi di storage
    (`photo_storage_keys`) e mai come binari. Per la modalita' measurements-only le foto
    sono assenti e si usa un avatar rappresentativo.
    """

    id: str = Field(default_factory=_new_id)
    user_id: str
    measurements: BodyMeasurements
    photo_storage_keys: list[str] = Field(
        default_factory=list,
        description="Chiavi storage (non URL pubblici) delle foto del corpo, se fornite.",
    )
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


# --------------------------------------------------------------------------- #
# Garment
# --------------------------------------------------------------------------- #
class Garment(DomainModel):
    """Capo normalizzato, pronto per la pipeline di try-on.

    Prodotto dal sottosistema di ingestion (da URL e-commerce o upload manuale).
    `size_chart` e' opzionale e usato dal fit engine, non dai provider di rendering.
    """

    id: str = Field(default_factory=_new_id)
    category: GarmentCategory
    image_url: str = Field(description="URL (firmato) dell'immagine prodotto normalizzata.")
    brand: Optional[str] = None
    title: Optional[str] = None
    color: Optional[str] = None
    source_url: Optional[str] = Field(
        default=None, description="URL e-commerce di provenienza (provenance)."
    )
    size_chart: Optional[dict[str, dict[str, float]]] = Field(
        default=None,
        description="Mappa taglia -> misure (es. {'M': {'chest_cm': 100}}). Usata dal fit engine.",
    )
    created_at: datetime = Field(default_factory=_utcnow)


# --------------------------------------------------------------------------- #
# Try-on contract (provider-agnostic)
# --------------------------------------------------------------------------- #
class TryOnRequest(DomainModel):
    """Input del contratto di rendering: `VirtualTryOnProvider.generate(TryOnRequest)`.

    Volutamente privo di parametri specifici di un fornitore. Gli adapter traducono
    questo contratto stabile nei parametri del provider concreto.

    Vincoli di modalita':
      - PHOTO_MEASUREMENTS richiede `person_image_url`.
      - MEASUREMENTS_ONLY richiede `avatar_image_url`.
    """

    mode: TryOnMode
    garment_image_url: str = Field(description="URL (firmato) dell'immagine del capo.")
    person_image_url: Optional[str] = Field(
        default=None, description="URL (firmato) della foto utente. Richiesto in PHOTO_MEASUREMENTS."
    )
    avatar_image_url: Optional[str] = Field(
        default=None, description="URL (firmato) dell'avatar. Richiesto in MEASUREMENTS_ONLY."
    )
    quality: TryOnQuality = Field(default=TryOnQuality.STANDARD)
    samples: int = Field(default=1, ge=1, le=4, description="Numero di immagini da generare.")
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Metadati non sensibili per tracciamento/idempotenza. Niente PII.",
    )

    @model_validator(mode="after")
    def _check_mode_inputs(self) -> "TryOnRequest":
        if self.mode is TryOnMode.PHOTO_MEASUREMENTS and not self.person_image_url:
            raise ValueError("person_image_url e' obbligatorio in modalita' photo_measurements")
        if self.mode is TryOnMode.MEASUREMENTS_ONLY and not self.avatar_image_url:
            raise ValueError("avatar_image_url e' obbligatorio in modalita' measurements_only")
        return self


class TryOnResult(DomainModel):
    """Output normalizzato del rendering, indipendente dal provider.

    `raw_response_ref` e' un riferimento (es. chiave storage) alla risposta grezza del
    provider, non il payload inline, per evitare di trascinare/loggare dati pesanti.
    """

    status: JobStatus
    provider: str = Field(description="Identificativo dell'adapter usato (es. 'mock', 'fashn').")
    output_image_urls: list[str] = Field(
        default_factory=list, description="URL (firmati) delle immagini generate."
    )
    model: Optional[str] = Field(default=None, description="Modello/versione del provider.")
    latency_ms: Optional[int] = Field(default=None, ge=0)
    cost_estimate: Optional[float] = Field(default=None, ge=0, description="Costo stimato del run.")
    raw_response_ref: Optional[str] = Field(
        default=None, description="Riferimento (non inline) alla risposta grezza del provider."
    )
    error: Optional[str] = Field(default=None, description="Messaggio d'errore se status=failed.")


class TryOnJob(DomainModel):
    """Unita' di lavoro asincrona: tracciata in DB, eseguita dal worker.

    Collega l'input (`request`) al risultato (`result`) e ne segue lo stato.
    """

    id: str = Field(default_factory=_new_id)
    user_id: str
    status: JobStatus = Field(default=JobStatus.QUEUED)
    request: TryOnRequest
    result: Optional[TryOnResult] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)
