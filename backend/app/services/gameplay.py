from app.domain.repository import ArtistRepository
from app.domain.game_logic import compare_artists
from app.domain.models import ArtistSchema 

class GameService:
    def __init__(self):
        self.repo = ArtistRepository()

    def start_new_game(self) -> ArtistSchema:
        return self.repo.get_random_valid_target()

    def process_guess(self, target_name: str, guess_name: str) -> dict:
        target = self.repo.get_by_name(target_name)
        guess = self.repo.get_by_name(guess_name)

        if not target or not guess:
            raise ValueError(f"Artiste introuvable")

        comparison = compare_artists(target, guess)
        guess_dict = guess.model_dump(by_alias=False)

        return {
            "guess_name": guess.name,
            "guess_artist": guess_dict,
            "is_win": (target.id == guess.id),
            "results": comparison
        }

    # --- MODIFICATION ICI ---
    def get_hint_data(self, target_name: str) -> dict:
        target = self.repo.get_by_name(target_name)
        if not target:
             raise ValueError("Artiste cible introuvable pour l'indice")
        
        # On renvoie Nationalité, Siècle ET Mouvement
        return {
            "nationality": target.nationality,
            "century": target.century,
            "movements": target.movements,
            "id": target.id # On renvoie l'ID pour que le front puisse chercher l'image de la cible
        }

    def search_artists(self, query: str) -> list[dict]:
        artists = self.repo.search_by_name(query)
        return [{"name": a.name, "id": a.id} for a in artists]