from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware # <--- 1. IMPORT IMPORTANT

from app.api.endpoint import router as game_router

app = FastAPI(title="Artdle", version="1.0.0")

# --- 2. CONFIGURATION CORS (INDISPENSABLE POUR LE FRONTEND SÉPARÉ) ---
# Cela permet à ton frontend (localhost, Netlify, etc.) de parler à ce backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" autorise tout le monde. C'est le plus simple pour ton projet.
    allow_credentials=True,
    allow_methods=["*"],  # Autorise GET, POST, etc.
    allow_headers=["*"],
)

# --- CONFIGURATION DES CHEMINS ---
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# --- GESTION DES IMAGES STATIQUES ---
# On garde ça, car ton frontend externe va chercher l'image de fond ici :
# https://artdle.onrender.com/static/piazza_de_italia.jpg
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- ROUTER API ---
app.include_router(game_router, prefix="/api/v1")

# --- ROUTE RACINE ---
# Tu peux garder ça, ça servira de "fallback" si on va direct sur l'URL Render
@app.get("/")
async def read_root():
    return FileResponse(FRONTEND_DIR / "index.html")