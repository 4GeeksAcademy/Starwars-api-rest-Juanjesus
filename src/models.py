from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


association_table1 = Table(
    "favorite_character",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("character_id", ForeignKey("character.id")),
)

association_table2 = Table(
    "favorite_planet",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("planet_id", ForeignKey("planet.id")),
)

association_table3 = Table(
    "favorite_vehicle",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("vehicle_id", ForeignKey("vehicle.id")),
)

class User(db.Model):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique = True, nullable = False)
    firstname: Mapped[str] = mapped_column(String(120), nullable = False)
    lastname: Mapped[str] = mapped_column(String(120), nullable = False)
    favorite_character: Mapped[List["Character"]] = relationship(
        "Character",
        secondary = association_table1,
        back_populates = "users_favorite_character"
    )
    favorite_planet: Mapped[List["Planet"]] = relationship(
        "Planet",
        secondary = association_table2,
        back_populates = "users_favorite_planet"
    )
    favorite_vehicle: Mapped[List["Vehicle"]] = relationship(
        "Vehicle",
        secondary = association_table3,
        back_populates = "users_favorite_vehicle"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "favorite_character": [character.serialize() for character in self.favorite_character],
            "favorite_planet": [planet.serialize() for planet in self.favorite_planet],
            "favorite_vehicle": [vehicle.serialize() for vehicle in self.favorite_vehicle]
        }

class Character(db.Model):

    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(120), nullable = False)
    quote: Mapped[str] = mapped_column(String(120))
    image: Mapped[str] = mapped_column(String(255))
    users_favorite_character: Mapped[List["User"]] = relationship(
        "User",
        secondary = association_table1,
        back_populates = "favorite_character"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image
        }
    
class Planet(db.Model):

    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(120), nullable = False)
    image: Mapped[str] = mapped_column(String(255))
    users_favorite_planet: Mapped[List["User"]] = relationship(
        "User",
        secondary = association_table2,
        back_populates = "favorite_planet"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image
        }

class Vehicle(db.Model):

    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(120), nullable = False)
    image: Mapped[str] = mapped_column(String(255))
    users_favorite_vehicle: Mapped[List["User"]] = relationship(
        "User",
        secondary = association_table3,
        back_populates = "favorite_vehicle"
    )
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image
        }