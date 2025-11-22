from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base

# --- Tables de relation many-to-many ---

r_artiste_mouvement = Table(
    "r_artiste_mouvement",
    Base.metadata,
    Column("artiste_id", ForeignKey("t_artiste.id"), primary_key=True),
    Column("mouvement_id", ForeignKey("t_mouvement.id"), primary_key=True),
)

r_oeuvre_genre = Table(
    "r_oeuvre_genre",
    Base.metadata,
    Column("oeuvre_id", ForeignKey("t_oeuvre.id"), primary_key=True),
    Column("genre_id", ForeignKey("t_genre.id"), primary_key=True),
)

# --- Tables principales ---

class Artiste(Base):
    __tablename__ = "t_artiste"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    sexe = Column(String(10), nullable=True)
    annee_naissance = Column(Integer, nullable=True)
    annee_mort = Column(Integer, nullable=True)
    nationalite = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    url_image_portrait = Column(Text, nullable=True)

    oeuvres = relationship("Oeuvre", back_populates="artiste")
    citations = relationship("Citation", back_populates="artiste")

    mouvements = relationship(
        "Mouvement",
        secondary=r_artiste_mouvement,
        back_populates="artistes",
    )


class Mouvement(Base):
    __tablename__ = "t_mouvement"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False, unique=True)
    periode = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    oeuvres = relationship("Oeuvre", back_populates="mouvement")
    artistes = relationship(
        "Artiste",
        secondary=r_artiste_mouvement,
        back_populates="mouvements",
    )


class Technique(Base):
    __tablename__ = "t_technique"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    oeuvres = relationship("Oeuvre", back_populates="technique")


class Structure(Base):
    __tablename__ = "t_structure"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    pays = Column(String(255), nullable=True)
    ville = Column(String(255), nullable=True)
    site_web = Column(String(255), nullable=True)

    oeuvres = relationship("Oeuvre", back_populates="structure")


class Genre(Base):
    __tablename__ = "t_genre"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    oeuvres = relationship(
        "Oeuvre",
        secondary=r_oeuvre_genre,
        back_populates="genres",
    )


class Oeuvre(Base):
    __tablename__ = "t_oeuvre"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    annee = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    url_image = Column(Text, nullable=False)
    identifiant_externe = Column(String(255), nullable=True)
    source = Column(String(255), nullable=True)

    artiste_id = Column(Integer, ForeignKey("t_artiste.id"), nullable=True)
    mouvement_id = Column(Integer, ForeignKey("t_mouvement.id"), nullable=True)
    technique_id = Column(Integer, ForeignKey("t_technique.id"), nullable=True)
    structure_id = Column(Integer, ForeignKey("t_structure.id"), nullable=True)

    artiste = relationship("Artiste", back_populates="oeuvres")
    mouvement = relationship("Mouvement", back_populates="oeuvres")
    technique = relationship("Technique", back_populates="oeuvres")
    structure = relationship("Structure", back_populates="oeuvres")

    genres = relationship(
        "Genre",
        secondary=r_oeuvre_genre,
        back_populates="oeuvres",
    )

    citations = relationship("Citation", back_populates="oeuvre")


class Citation(Base):
    __tablename__ = "t_citation"

    id = Column(Integer, primary_key=True, index=True)
    texte = Column(Text, nullable=False)
    langue = Column(String(10), nullable=True)
    source_reference = Column(String(255), nullable=True)
    annee = Column(Integer, nullable=True)

    artiste_id = Column(Integer, ForeignKey("t_artiste.id"), nullable=True)

    artiste = relationship("Artiste", back_populates="citations")
