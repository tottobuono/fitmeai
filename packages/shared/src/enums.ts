/**
 * Enum di dominio condivisi (literal union types).
 *
 * I valori stringa sono il contratto effettivo sul filo e devono combaciare 1:1
 * con gli enum Pydantic in `apps/api/app/domain/enums.py`.
 */

export const TryOnMode = {
  PHOTO_MEASUREMENTS: "photo_measurements",
  MEASUREMENTS_ONLY: "measurements_only",
} as const;
export type TryOnMode = (typeof TryOnMode)[keyof typeof TryOnMode];

export const JobStatus = {
  QUEUED: "queued",
  PROCESSING: "processing",
  DONE: "done",
  FAILED: "failed",
  CANCELED: "canceled",
} as const;
export type JobStatus = (typeof JobStatus)[keyof typeof JobStatus];

export const GarmentCategory = {
  TOP: "top",
  BOTTOM: "bottom",
  DRESS: "dress",
  OUTERWEAR: "outerwear",
  OTHER: "other",
} as const;
export type GarmentCategory = (typeof GarmentCategory)[keyof typeof GarmentCategory];

export const MeasurementUnit = {
  METRIC: "metric",
  IMPERIAL: "imperial",
} as const;
export type MeasurementUnit = (typeof MeasurementUnit)[keyof typeof MeasurementUnit];

export const FitPreference = {
  SLIM: "slim",
  REGULAR: "regular",
  RELAXED: "relaxed",
} as const;
export type FitPreference = (typeof FitPreference)[keyof typeof FitPreference];

export const TryOnQuality = {
  PREVIEW: "preview",
  STANDARD: "standard",
  HIGH: "high",
} as const;
export type TryOnQuality = (typeof TryOnQuality)[keyof typeof TryOnQuality];
