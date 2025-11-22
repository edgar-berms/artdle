from fastapi import FastAPI

from app.core.config import settings
from app.infrastructure.db.base import Base, engine
from app.infrastructure.db import models  # important pour que les tables soient connues
from app.api.routers import health


# Création des tables si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Artdle API",
    version="0.1.0",
    debug=settings.DEBUG,
)

# Routes
app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Artdle", "env": settings.ENVIRONMENT}
