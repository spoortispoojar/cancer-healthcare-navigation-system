
from fastapi import FastAPI

from app.routes import router


app = FastAPI(
    title="Cancer Healthcare Navigation System",
    description=(
        "Backend API for healthcare navigation "
        "and support services for breast and lung "
        "cancer patients. This is not a cancer "
        "diagnosis system."
    ),
    version="1.0.0",
)

# Register assessment routes
app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Cancer Healthcare Navigation API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
