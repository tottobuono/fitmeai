"""Enum di dominio condivisi.

I valori (stringhe) sono il contratto effettivo sul filo: devono combaciare 1:1 con i
literal union types definiti in `packages/shared`.
"""

from enum import Enum


class TryOnMode(str, Enum):
    """Modalita' d'uso del prodotto."""

    PHOTO_MEASUREMENTS = "photo_measurements"  # foto utente + misure
    MEASUREMENTS_ONLY = "measurements_only"  # solo misure -> avatar rappresentativo


class JobStatus(str, Enum):
    """Stato del ciclo di vita di un job di try-on."""

    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    CANCELED = "canceled"


class GarmentCategory(str, Enum):
    """Categoria del capo, rilevante per il try-on."""

    TOP = "top"
    BOTTOM = "bottom"
    DRESS = "dress"
    OUTERWEAR = "outerwear"
    OTHER = "other"


class MeasurementUnit(str, Enum):
    """Sistema di unita' delle misure corporee."""

    METRIC = "metric"  # cm / kg
    IMPERIAL = "imperial"  # in / lb


class FitPreference(str, Enum):
    """Preferenza di vestibilita' dichiarata dall'utente (separata dai dati corporei)."""

    SLIM = "slim"
    REGULAR = "regular"
    RELAXED = "relaxed"


class TryOnQuality(str, Enum):
    """Livello qualitativo del rendering richiesto al provider."""

    PREVIEW = "preview"
    STANDARD = "standard"
    HIGH = "high"
