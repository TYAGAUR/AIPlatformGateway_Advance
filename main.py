from fastapi import FastAPI

from api.endpoints import router


app = FastAPI(
    title="AI Platform Gateway",
    description="API for managing AI models and processing AI requests",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Welcome to AI Platform Gateway",
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Platform Gateway"
    }


app.include_router(router)