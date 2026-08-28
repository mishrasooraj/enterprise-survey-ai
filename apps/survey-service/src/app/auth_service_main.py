from fastapi import FastAPI

from app.api.api_router import api_router
from app.db import models  # noqa: F401


app = FastAPI(
    title="Enterprise Survey AI - Survey Service",
    description="Survey lifecycle service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(api_router)

