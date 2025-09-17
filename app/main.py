from fastapi import FastAPI
from app.router import router as app_router

# Create FastAPI instance
app = FastAPI(
    title="Newfold Image Processing API",
    description="A simple API for image processing with ImageMagick",
    version="1.0.0"
)

# Include app router
app.include_router(app_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Newfold Image Processing API",
        "status": "Running 🚀",
        "docs": "/docs",
    }

