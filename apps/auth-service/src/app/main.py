from fastapi import FastAPI
from app.lifespan import lifespan   

from app.api.router import api_router
from app.db import models  # noqa: F401


app = FastAPI(
    title="Enterprise Survey AI - Authentication Service",
    description="Authentication and Identity Management Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router)
