
from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Cancer Healthcare Navigation API",
    description="Healthcare support and facility recommendation system",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Cancer Healthcare Navigation API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
