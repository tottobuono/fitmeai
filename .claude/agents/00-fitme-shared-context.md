# Fitme.ai shared context

## Mission
Fitme.ai is an AI-native fashion startup focused on helping users understand how clothes will look and fit on their body before buying online.

## Product modes
### Mode 1 — Photo + measurements
The user uploads one or two body photos and enters body measurements such as height, weight, chest, waist, hips, and fit preference. The system generates photorealistic try-on images using external virtual try-on APIs and also produces size and fit insights.

### Mode 2 — Measurements only
If the user does not want to upload personal photos, the system uses body measurements to select or generate a body avatar or representative body model, then renders the garment on that body representation and still provides fit and sizing insights.

## Core product goals
- Deliver a realistic preview of garments from ecommerce sources such as Zara or Nike.
- Keep costs low enough for an MVP by relying on external APIs rather than local model hosting.
- Build a provider-agnostic architecture so the team can switch virtual try-on models later.
- Separate image rendering from fit intelligence.
- Be privacy-conscious and designed for GDPR and AI Act compliance from the beginning.

## Suggested architecture principles
- Frontend app for onboarding, garment input, result display.
- Backend API for users, body profiles, products, jobs, auth, storage orchestration.
- Virtual try-on abstraction layer with swappable providers.
- Body profile and fit engine for measurements, sizing, and avatar logic.
- Compliance layer for consent, retention, deletion, auditability.

## Working rules for all agents
- Optimize for an MVP that can be built in 2–3 months.
- Prefer simple, production-friendly decisions over academic complexity.
- Avoid local model training or hosting unless explicitly requested.
- Produce concrete code, interfaces, file structures, migrations, endpoint specs, and task breakdowns.
- When unsure, choose modularity and ease of replacement over clever shortcuts.
- Assume the target stack can be Next.js on the frontend, FastAPI on the backend, PostgreSQL, object storage, and queue-based async jobs.
- Treat body photos and body measurements as sensitive personal data.
- Keep outputs implementation-ready, not just conceptual.
