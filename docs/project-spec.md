# Qatar Accessibility Mapper — Project Specification

> This spec is the implementation source of truth. It adapts the planning document created before the repository existed.

## One-line pitch

An evidence-backed map that helps people discover venues with useful accessibility information, while clearly showing what is known, what is inferred, and what still needs verification.

## Goals and non-goals

**Goals**
- Search and map public venues in a small, well-defined Doha pilot area.
- Display accessibility facts with provenance, freshness, and confidence.
- Combine volunteered/official structured facts with carefully reviewed image-derived suggestions.
- Allow users to correct stale or incorrect facts.

**Non-goals for the first release**
- Claim to certify a venue as accessible or guarantee a route is safe.
- Infer personal disability status or collect sensitive user profiles.
- Crawl image sites or reuse imagery without clear rights and permission.
- Cover all of Qatar before the pilot workflow is validated.

## Users and core workflow

Primary users are residents and visitors who need to compare venues before visiting. A user filters the map by venue type and specific features (step-free entrance, elevator, accessible toilet, parking, etc.), opens a venue card, inspects each claim and its source/date, then optionally submits a correction.

## Data sources

- [OpenStreetMap Qatar extract on Geofabrik](https://download.geofabrik.de/asia/qatar.html) for venue/road geometry and OSM tags. OSM is ODbL; attribute and display attribution, retain source identifiers, and review share-alike obligations before distributing derived databases.
- [OpenStreetMap wiki: Accessibility](https://wiki.openstreetmap.org/wiki/Key:wheelchair) for tag semantics such as `wheelchair=yes|limited|no` and `toilets:wheelchair`.
- Optional official/open Qatar venue data, if a suitable dataset with clear reuse terms is found. Record its license and provider. Do not assume commercial map API terms permit dataset redistribution.
- Optional imagery only from sources with an explicit reuse/license basis or images submitted with informed consent. The MVP can be completed without image inference: start with OSM tags plus a small, manually verified pilot set.

## Desired stack

- Python 3.12, Pandas, GeoPandas, Shapely, OSMnx/pyrosm for local extraction and processing.
- PostgreSQL + PostGIS for spatial storage and queries.
- FastAPI + Pydantic for a typed API; SQLAlchemy/Alembic for persistence and migrations.
- React + TypeScript + MapLibre GL JS for the map UI (or a Streamlit prototype in week one).
- Optional image inference: a vision-language model behind an adapter interface, with model/version recorded; never use its output as confirmed truth.
- pytest, Ruff, pre-commit, GitHub Actions, Docker Compose. Add an error tracker only if a hosted demo needs it.

## Features

### MVP
- Interactive pilot-area map with filters for venue type and individual accessibility features.
- Venue detail card listing value, evidence type, source, last-checked date, and confidence/status.
- Status vocabulary: `verified`, `osm_reported`, `model_suggested`, `unknown`, `conflicting`, `stale`.
- Admin/reviewer screen to accept, reject, or edit claims; public correction form with moderation queue.
- CSV/GeoJSON import command with schema checks, deduplication, and idempotent updates.
- Basic usage documentation, data attribution, privacy statement, and known limitations.

### Stretch
- Route-aware pedestrian context using OSM paths and crossings, clearly labeled as experimental.
- Evidence image workflow with consent/license metadata and human review.
- Temporal freshness reminders; confidence calibration; Arabic and English UI.

## Data model and handling

Store a venue separately from claims. Suggested tables: `venue(id, source, source_id, name, category, geom, updated_at)`, `claim(id, venue_id, feature, value, status, source_type, source_uri, evidence_id, observed_at, reviewer_id, model_version, confidence)`, `evidence(id, storage_key, license_or_consent, captured_at, retention_until)` and `correction(id, claim_id, proposed_value, created_at, review_status)`. Keep original source records in a raw/staging area and derive normalized records in a repeatable pipeline.

- Preserve OSM object IDs and attribution; keep a source/ingestion timestamp and source license with every imported batch.
- Validate coordinates, allowed tags, geometries, duplicate IDs, and impossible feature/value combinations. Quarantine failures instead of silently dropping them.
- Do not scrape or persist personal data. Avoid retaining submitter contact details; if contact is needed, make it optional and delete after moderation.
- Do not store submitted photos until rights/consent are recorded. Strip EXIF location/device metadata unless explicitly required and consented to.
- Version data snapshots used in experiments. Keep train/validation/test venue splits geographically separated to reduce spatial leakage.
- Treat model output as a suggestion. A model must not overwrite an existing verified claim.

## Logic and pipeline

1. **Acquire:** download a dated Qatar OSM extract and optionally import approved official/open sources.
2. **Validate:** check schema, license metadata, coordinate system, geometry validity, and required identifiers; report rejected rows.
3. **Normalize:** map OSM tags into a stable feature ontology. Keep raw tags alongside normalized values; do not convert missing tags into `no`.
4. **Resolve entities:** deduplicate by stable source IDs first; use proximity/name matching only as a candidate list for review.
5. **Enrich (optional):** run image models only on permitted images. Produce feature candidates and evidence references, not final truth.
6. **Review:** reviewer confirms, rejects, or edits candidates. Record the reviewer and timestamp.
7. **Serve:** store approved/current claims in PostGIS. Spatial queries return nearby venues and filter against explicit feature states.
8. **Feedback:** create correction records, moderate them, then append a new claim version rather than overwriting the audit trail.

## Evaluation

This is a data product plus optional model; report system and model quality separately.

- **Extraction/normalization:** tag mapping accuracy on a manually checked sample; parse/validation acceptance rate; duplicate rate; percent of source rows with preserved provenance.
- **Venue discovery:** precision@k for search results and coverage (% of known pilot venues surfaced); measure by venue category.
- **Accessibility claim quality:** precision, recall, and F1 per feature against an independently labeled, consented pilot set. Report unknown coverage separately; do not score unknown as negative. Show confusion matrix and inter-annotator agreement (Cohen's kappa for two annotators).
- **Image suggestion model (if included):** per-feature precision/recall/F1, PR-AUC where useful, calibration (Brier score/ECE), and false-positive rate. Favor precision for safety-relevant positive claims; threshold per feature on validation data.
- **Freshness:** fraction of claims older than chosen freshness windows and correction resolution time.
- **Product quality:** API p95 latency, map query latency, correction submission/review completion rate.
- **No unsupported overall “accessibility score”** in MVP. If a summary is added later, define its formula, missing-data behavior, and validate it with users.

## Plan and milestones

1. **Scope/data audit (2–3 days):** choose one Doha pilot area and 3–5 concrete features; inspect OSM coverage, license, and tag quality; write ontology and data dictionary.
2. **Data pipeline (3–5 days):** import, validate, normalize, deduplicate; publish a reproducible snapshot manifest and quality report.
3. **API and spatial storage (3–5 days):** PostGIS schema, migrations, spatial/filter endpoints, automated tests.
4. **Map MVP (4–6 days):** filters, detail cards, provenance/status UI, responsive layout.
5. **Review loop (3–4 days):** correction queue, append-only claim history, moderation and privacy controls.
6. **Evaluation (3–5 days):** create double-labeled pilot set; calculate metrics and analyze errors by feature/category.
7. **Demo/readme (2 days):** deploy a small demo, document limitations, licenses, setup, architecture, and a short walkthrough.

## Acceptance criteria

- Re-running import on the same snapshot is idempotent and emits a quality report.
- The UI never presents a missing tag as evidence that a venue lacks a feature.
- Every displayed claim has a status and provenance or is explicitly marked unknown.
- Corrections are auditable; model suggestions cannot replace verified claims.
- Results include labeled-set size, annotation procedure, per-feature metrics, and limitations.
