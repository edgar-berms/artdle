from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, List, Union

class ComparisonResult(BaseModel):
    field: str
    value: Union[str, int, List[str], None]
    status: Literal["CORRECT", "WRONG", "HIGHER", "LOWER", "PARTIAL"]

class ArtistSchema(BaseModel):
    id: str = Field(alias="idFormatted")
    name: str = Field(alias="nom_unique")
    sex: str = Field(alias="sexe")
    nationality: str = Field(alias="nationalites")
    movements: str = Field(alias="mouvements")
    professions: str = Field(alias="metiers")
    
    # On accepte que ce soit None par défaut
    birth_year: Optional[int] = Field(None, alias="date_naissance")
    death_year: Optional[int] = Field(None, alias="date_mort")
    
    popularity: int = Field(alias="popularite")

    @field_validator('birth_year', 'death_year', mode='before')
    def parse_year(cls, v):
        # Si c'est vide, None ou une chaine vide
        if v is None or v == "": 
            return None
        try:
            # On tente de prendre les 4 premiers chiffres
            # Ex: "1974 (environ)" -> 1974
            return int(str(v)[:4])
        except (ValueError, TypeError):
            # Si c'est "Inconnu" ou du texte bizarre, on renvoie None
            return None

    @property
    def century(self) -> int:
        if not self.birth_year:
            return 0
        return (self.birth_year - 1) // 100 + 1