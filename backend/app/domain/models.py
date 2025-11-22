from dataclasses import dataclass
from typing import Optional

# TODO exemple à modifier
@dataclass
class Artwork:
    id: Optional[int]
    source: str
    external_id: str
    title: str
    artist: str
    year: Optional[str]
    image_url: str
    description: Optional[str] = None
