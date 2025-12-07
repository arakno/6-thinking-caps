"""Main FastAPI application."""
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api.routes import router
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="6 Thinking Hats Multi-Agent Analysis System",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix=settings.api_prefix, tags=["sessions"])

# Get static files directory
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)

# Mount static files if they exist
if static_dir.exists() and any(static_dir.iterdir()):
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def root():
    """Serve React app or landing page."""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "message": "6 Thinking Hats Multi-Agent System",
        "status": "API is running",
        "docs": "/docs",
    }


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve React app for all non-API routes (SPA catch-all)."""
    # Don't interfere with API routes or static assets
    if full_path.startswith("api/") or full_path.startswith("static/"):
        return None
    
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"detail": "Not found"}


@app.on_event("startup")
async def startup_event():
    """Run on app startup."""
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown."""
    logger.info(f"Shutting down {settings.app_name}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
