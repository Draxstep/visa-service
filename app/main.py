from fastapi import FastAPI

from app.api.v1.routes import router as api_v1_router
from app.core.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
