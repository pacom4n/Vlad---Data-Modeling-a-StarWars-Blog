from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import PrimaryKeyConstraint

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)

    favorite_characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary="favorite_character",
        back_populates="favorited_by"
    )
    
    favorite_planets: Mapped[list["Planet"]] = relationship(
        "Planet",
        secondary="favorite_planet",
        back_populates="favorited_by"
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=True)
    mass: Mapped[float] = mapped_column(Float, nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(Enum('male', 'female', 'n/a', 'hermaphrodite', name='gender_enum'), nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary="favorite_character",
        back_populates="favorite_characters"
    )

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    diameter: Mapped[int] = mapped_column(Integer, nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary="favorite_planet",
        back_populates="favorite_planets"
    )

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "population": self.population,
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), primary_key=True)

    __table_args__ = (PrimaryKeyConstraint('user_id', 'character_id'),)

    def __repr__(self):
        return f'<Favorite: User {self.user_id} likes Character {self.character_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), primary_key=True)

    __table_args__ = (PrimaryKeyConstraint('user_id', 'planet_id'),)

    def __repr__(self):
        return f'<Favorite: User {self.user_id} likes Planet {self.planet_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }