/**
 * Modelli di dominio condivisi (contratti) di Fitme.ai.
 *
 * Devono restare coerenti con i modelli Pydantic in `apps/api/app/domain/models.py`.
 * I campi usano `snake_case` per combaciare esattamente con il JSON dell'API.
 *
 * Nota privacy: i campi `*_url` sono URL firmati a breve scadenza o riferimenti a
 * storage, mai binari, e non vanno loggati in chiaro.
 */

import type {
  FitPreference,
  GarmentCategory,
  JobStatus,
  MeasurementUnit,
  TryOnMode,
  TryOnQuality,
} from "./enums.js";

/** Misure corporee canoniche (rappresentazione interna in cm/kg). */
export interface BodyMeasurements {
  height_cm: number;
  weight_kg: number;
  chest_cm?: number | null;
  waist_cm?: number | null;
  hips_cm?: number | null;
  inseam_cm?: number | null;
  unit: MeasurementUnit;
  fit_preference: FitPreference;
}

/** Profilo corporeo. Le foto sono solo riferimenti a storage, mai binari inline. */
export interface BodyProfile {
  id: string;
  user_id: string;
  measurements: BodyMeasurements;
  photo_storage_keys: string[];
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}

/** Capo normalizzato, pronto per la pipeline di try-on. */
export interface Garment {
  id: string;
  category: GarmentCategory;
  image_url: string;
  brand?: string | null;
  title?: string | null;
  color?: string | null;
  source_url?: string | null;
  /** Mappa taglia -> misure, es. { M: { chest_cm: 100 } }. Usata dal fit engine. */
  size_chart?: Record<string, Record<string, number>> | null;
  created_at: string; // ISO 8601
}

/**
 * Input del contratto di rendering provider-agnostic.
 * Vincoli: photo_measurements richiede `person_image_url`;
 * measurements_only richiede `avatar_image_url`.
 */
export interface TryOnRequest {
  mode: TryOnMode;
  garment_image_url: string;
  person_image_url?: string | null;
  avatar_image_url?: string | null;
  quality: TryOnQuality;
  samples: number; // 1..4
  metadata: Record<string, string>;
}

/** Output normalizzato del rendering, indipendente dal provider. */
export interface TryOnResult {
  status: JobStatus;
  provider: string;
  output_image_urls: string[];
  model?: string | null;
  latency_ms?: number | null;
  cost_estimate?: number | null;
  raw_response_ref?: string | null;
  error?: string | null;
}

/** Unita' di lavoro asincrona tracciata in DB ed eseguita dal worker. */
export interface TryOnJob {
  id: string;
  user_id: string;
  status: JobStatus;
  request: TryOnRequest;
  result?: TryOnResult | null;
  error?: string | null;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}
