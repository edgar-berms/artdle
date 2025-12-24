# --- CORRECTION DE L'IMPORT ---
# On ajoute ".models" car tes classes sont dans models.py
from app.domain.models import ArtistSchema, ComparisonResult

def compare_sets(target_val: str, guess_val: str) -> str:
    """Retourne CORRECT, PARTIAL ou WRONG"""
    if not target_val or not guess_val:
        return "CORRECT" if target_val == guess_val else "WRONG"

    t_set = set(x.strip().lower() for x in target_val.split(','))
    g_set = set(x.strip().lower() for x in guess_val.split(','))

    if t_set == g_set:
        return "CORRECT"
    elif not t_set.isdisjoint(g_set):
        return "PARTIAL"
    else:
        return "WRONG"

def compare_numbers(target_val: int, guess_val: int) -> str:
    """Retourne CORRECT, HIGHER ou LOWER"""
    if guess_val == target_val:
        return "CORRECT"
    elif guess_val < target_val:
        return "HIGHER" # La cible est plus grande
    else:
        return "LOWER"  # La cible est plus petite

def compare_artists(target: ArtistSchema, guess: ArtistSchema) -> dict[str, ComparisonResult]:
    results = {}

    # 1. Sexe (Strict)
    results["sex"] = ComparisonResult(
        field="sex", value=guess.sex,
        status="CORRECT" if guess.sex.lower() == target.sex.lower() else "WRONG"
    )

    # 2. Nationalité (Set)
    results["nationality"] = ComparisonResult(
        field="nationality", value=guess.nationality,
        status=compare_sets(target.nationality, guess.nationality)
    )

    # 3. Mouvements (Set)
    results["movements"] = ComparisonResult(
        field="movements", value=guess.movements,
        status=compare_sets(target.movements, guess.movements)
    )

    # 4. Métiers (Set)
    results["professions"] = ComparisonResult(
        field="professions", value=guess.professions,
        status=compare_sets(target.professions, guess.professions)
    )

    # 5. Année de Naissance (Numérique)
    results["birth_year"] = ComparisonResult(
        field="birth_year", value=guess.birth_year,
        status=compare_numbers(target.birth_year, guess.birth_year)
    )

    # 6. Siècle (Numérique)
    results["century"] = ComparisonResult(
        field="century", value=guess.century,
        status=compare_numbers(target.century, guess.century)
    )

    # 7. Popularité (Numérique)
    results["popularity"] = ComparisonResult(
        field="popularity", value=guess.popularity,
        status=compare_numbers(target.popularity, guess.popularity)
    )

    # 8. Date de mort (Gestion des vivants/morts + Numérique)
    death_status = "WRONG"
    if guess.death_year == target.death_year:
        death_status = "CORRECT"
    elif guess.death_year is not None and target.death_year is not None:
        # Les deux sont morts, on compare
        death_status = compare_numbers(target.death_year, guess.death_year)
    
    results["death_year"] = ComparisonResult(
        field="death_year", value=guess.death_year, status=death_status
    )

    return results