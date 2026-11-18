# Ingestion pipeline

The ingestion pipeline is planned but not implemented. The first version should download a dated Qatar OSM extract, retain source IDs and license metadata, validate geometries/tags, normalize accessibility fields without converting missing tags to `no`, and write an auditable quality report. See [`../../docs/project-spec.md`](../../docs/project-spec.md).

Do not commit raw OSM extracts or derived bulk data to this repository.
