# Fichier: backend/app/core/config.py

class Settings:
    PROJECT_NAME: str = "Artdle"
    DEBUG: bool = True
    ENVIRONMENT: str = "local"

# On instancie la classe pour pouvoir l'importer ailleurs
settings = Settings()