import json
import random
import os
from pathlib import Path
from typing import List, Optional

# --- CORRECTION ICI ---
# 1. On précise 'app.domain' car le dossier domain est dans app
# 2. On précise '.models' car ton fichier s'appelle models.py
from app.domain.models import ArtistSchema

class ArtistRepository:
    def __init__(self):
        # Calcul dynamique du chemin pour trouver le JSON
        # On part de: backend/app/domain/repository.py
        current_dir = Path(__file__).resolve().parent
        
        # On remonte : domain -> app -> backend -> ARTDLE -> ressources
        self.file_path = current_dir.parent.parent.parent / "ressources" / "artistes_final.json"
        
        # Debug
        print(f"📂 Repository init. Chemin JSON: {self.file_path}")

        self._data: List[ArtistSchema] = []
        self._load_data()

    def _load_data(self):
        if not self.file_path.exists():
            print(f"❌ ERREUR : Fichier introuvable à : {self.file_path}")
            return

        print(f"📂 Lecture du fichier : {self.file_path}")

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                print(f"🔍 Le JSON brut contient {len(raw_data)} éléments.")

                for i, item in enumerate(raw_data):
                    try:
                        artist = ArtistSchema(**item)
                        self._data.append(artist)
                    except Exception as e:
                        # AFFICHE L'ERREUR POUR LE PREMIER ÉLÉMENT SEULEMENT (pour pas spammer)
                        if i == 0:
                            print(f"❌ ERREUR CRITIQUE sur le 1er artiste : {e}")
                            print(f"Données reçues : {item}")
                        continue
                        
            print(f"✅ Résultat final : {len(self._data)} artistes valides chargés.")
            
        except Exception as e:
            print(f"❌ Erreur globale lecture JSON : {e}")

    def search_by_name(self, query: str, limit: int = 5) -> List[ArtistSchema]:
        query = query.lower().strip()
        results = []
        for artist in self._data:
            if query in artist.name.lower():
                results.append(artist)
                if len(results) >= limit:
                    break
        return results

    def get_by_name(self, name: str) -> Optional[ArtistSchema]:
        for artist in self._data:
            if artist.name.lower() == name.lower():
                return artist
        return None

    def get_random_valid_target(self) -> ArtistSchema:
        valid_candidates = [
            a for a in self._data
            if a.nationality and a.nationality.strip() != ""
            and a.movements and a.movements.strip() != ""
            and a.professions and a.professions.strip() != ""
            and a.birth_year is not None
        ]
        
        if not valid_candidates:
            if not self._data:
                # Évite le crash si la liste est vide au démarrage (ex: mauvais chemin json)
                print("⚠️ Base vide, impossible de choisir une cible.")
                raise Exception("Base de données vide")
            return random.choice(self._data)
            
        return random.choice(valid_candidates)