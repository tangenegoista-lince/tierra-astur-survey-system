from fastapi import FastAPI
from app.api.v1.endpoints import surveys
from app.core.config import settings

app = FastAPI(
    title="Tierra Astur Survey Card Data Extraction System",
    description="API for processing physical survey cards and extracting structured data",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(surveys.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Tierra Astur Survey Card Data Extraction System API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
