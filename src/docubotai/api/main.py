"""
DocuBotAI API server for the RAG system.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from docubotai import __version__
from docubotai.api.routes import tools, scraping, query, admin
from docubotai.core.config import settings

app = FastAPI(
    title="DocuBotAI",
    description="Documentation agent that auto-scrapes toolstacks and creates a RAG system",
    version=__version__,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Maintenance mode middleware
@app.middleware("http")
async def maintenance_mode_middleware(request, call_next):
    """Check if system is in maintenance mode."""
    if os.getenv("MAINTENANCE_MODE", "false").lower() == "true":
        if request.url.path != "/health":
            return JSONResponse(
                status_code=503,
                content={
                    "detail": os.getenv(
                        "MAINTENANCE_MESSAGE",
                        "System is under maintenance"
                    )
                }
            )
    return await call_next(request)

# Include routers
app.include_router(tools.router)
app.include_router(scraping.router)
app.include_router(query.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    """Root endpoint returning service information."""
    return {
        "name": "DocuBotAI",
        "version": __version__,
        "status": "operational",
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}