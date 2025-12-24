from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.gameplay import GameService 

router = APIRouter()

# --- DÉPENDANCES ---
def get_game_service():
    return GameService()

# --- MODÈLES (SCHEMAS) ---
class ArtistSearchItem(BaseModel):
    name: str
    id: str

class GuessRequest(BaseModel):
    target_name: str
    guess_name: str

# NOUVEAU : Modèle pour demander un indice
class HintRequest(BaseModel):
    target_name: str

# --- ROUTES ---

@router.get("/game/start")
def start_game(service: GameService = Depends(get_game_service)):
    """Démarre une partie en choisissant un artiste aléatoire"""
    try:
        target = service.start_new_game()
        return {
            "message": "Game started",
            "target_name_encrypted": target.name,
            "target_id_encrypted": target.id
        }
    except Exception as e:
        print(f"Erreur start_game: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/game/guess")
def make_guess(
    request: GuessRequest, 
    service: GameService = Depends(get_game_service)
):
    """Compare le guess du joueur avec la cible"""
    try:
        result = service.process_guess(request.target_name, request.guess_name)
        return result
    except ValueError as e:
        # Artiste non trouvé (404)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Erreur make_guess: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# NOUVELLE ROUTE : Obtenir un indice
@router.post("/game/hint")
def get_hint(
    request: HintRequest,
    service: GameService = Depends(get_game_service)
):
    """Renvoie des indices fixes sur la cible"""
    try:
        hint_data = service.get_hint_data(request.target_name)
        return hint_data
    except ValueError as e:
         raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Erreur hint: {e}")
        raise HTTPException(status_code=500, detail="Impossible de récupérer l'indice")


@router.get("/artists/search", response_model=List[ArtistSearchItem])
def search_artists(
    q: str, 
    service: GameService = Depends(get_game_service)
):
    """Appelé pour l'autocomplete."""
    if not q or len(q) < 2:
        return [] 
    return service.search_artists(q)