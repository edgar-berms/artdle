from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# On garde l'import du routeur
from app.api.endpoint import router as game_router

# --- CORRECTION : On définit l'app directement sans passer par "settings" ---
app = FastAPI(title="Artdle", version="1.0.0")

# --- CONFIGURATION DES CHEMINS ---
# On récupère le dossier parent du dossier 'backend' pour trouver 'frontend'
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# --- LA LIGNE MAGIQUE POUR L'IMAGE ---
# Autorise l'accès aux images du dossier frontend via /static
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- ROUTER API ---
# On met le préfixe en dur pour éviter tout bug de config
app.include_router(game_router, prefix="/api/v1")

# --- ROUTE RACINE (ACCUEIL) ---
@app.get("/")
async def read_root():
    # Sert le fichier index.html principal
    return FileResponse(FRONTEND_DIR / "index.html")