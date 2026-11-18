"""Minimal API scaffold; data endpoints will be added with the MVP pipeline."""

from fastapi import FastAPI

app = FastAPI(
    title="Qatar Accessibility Mapper API",
    description=(
        "Evidence-backed accessibility information. The API must distinguish "
        "verified claims from source-reported, suggested, unknown, and stale data."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    """Return a lightweight process health response."""
    return {"status": "ok"}
