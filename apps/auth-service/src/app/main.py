from fastapi import FastAPI


app = FastAPI(
    title="Enterprise Survey AI - Authentication Service",
    description="Authentication and Identity Management Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)