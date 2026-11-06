from fastapi import FastAPI

app = FastAPI(
    title="MediVault API",
    description="Backend API for the MediVault family medical-record platform.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return a basic process health status."""
    return {"status": "ok"}
