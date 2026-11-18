# Qatar Accessibility Mapper

An evidence-backed map for exploring accessibility information about public venues in Qatar. The project distinguishes verified facts from source-reported tags, model suggestions, unknowns, conflicts, and stale information. It is a portfolio project and does not certify venues or guarantee accessibility.

## Project status

**Planning / scaffold.** The initial scope, data model, pipeline, and evaluation plan are in [`docs/project-spec.md`](docs/project-spec.md). The implementation will begin with a small Doha pilot area and OpenStreetMap data. No venue accessibility claims are currently published by this repository.

## Planned MVP

- Import and normalize a dated OpenStreetMap Qatar extract.
- Store venues and claim provenance in PostgreSQL/PostGIS.
- Provide a FastAPI interface and MapLibre map with feature filters.
- Show source, observed date, and status for every claim; missing tags remain unknown.
- Add a moderated correction workflow and reproducible data quality report.

## Planned stack

Python, GeoPandas, Shapely, OSMnx/pyrosm, PostgreSQL + PostGIS, FastAPI, Pydantic, React + TypeScript, MapLibre GL JS, Docker Compose, pytest, Ruff, and GitHub Actions.

## Data and attribution

The planned starting data source is the [Geofabrik Qatar OpenStreetMap extract](https://download.geofabrik.de/asia/qatar.html). OpenStreetMap data is available under the [Open Database License (ODbL)](https://www.openstreetmap.org/copyright). A future deployed map must include appropriate attribution, preserve source identifiers and timestamps, and review ODbL obligations for derived datasets. Do not add venue imagery unless its reuse rights or informed consent are recorded.

## Development

The application and ingestion pipeline are not implemented yet. Follow the milestones in the spec. Raw data should be downloaded locally and excluded from Git; commit code, small synthetic fixtures, and data manifests only.

## Safety and limitations

- A missing tag is not evidence that a venue lacks an accessibility feature.
- Model-generated observations are suggestions and require human review.
- The project must not present an overall accessibility certification or score in the MVP.
- Coverage is limited to the chosen pilot and available source data.

## License

No software license has been selected yet. Add one before accepting external contributions or redistributing the code. Dataset licenses remain separate from the software license.
