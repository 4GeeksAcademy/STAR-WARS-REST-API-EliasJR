from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    favorites = db.relationship("FavoriteItem", back_populates="user")

    def __repr__(self):
        return f'<User {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
        }

class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }

class Planet(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    surface_water = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "gravity": self.gravity,
            "surface_water": self.surface_water,
        }

class Starship(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(50), nullable=False)  # Adjusted to String
    manufacturer = db.Column(db.String(50), nullable=False)
    cost_in_credits = db.Column(db.String(50), nullable=False)
    length = db.Column(db.String(50), nullable=False)
    max_atmosphering_speed = db.Column(db.String(50), nullable=False)
    crew = db.Column(db.String(50), nullable=False)
    passengers = db.Column(db.String(50), nullable=False)
    cargo_capacity = db.Column(db.String(50), nullable=False)
    consumables = db.Column(db.String(50))  # Added missing column
    hyperdrive_rating = db.Column(db.String(50))  # Added missing column
    mglt = db.Column(db.String(50))  # Added missing column
    starship_class = db.Column(db.String(50))  # Added missing column

    def __repr__(self):
        return f'<Starship {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.mglt,
            "starship_class": self.starship_class,
        }

class FavoriteItem(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    attribute1 = db.Column(db.String(100))
    attribute2 = db.Column(db.String(100))

    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    starship_id = db.Column(db.Integer, db.ForeignKey("starships.id"))

    user = db.relationship("User", back_populates="favorites")
    character = db.relationship("Character")
    planet = db.relationship("Planet")
    starship = db.relationship("Starship")

    def __repr__(self):
        return f'<FavoriteItem {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "name": self.name,
            "attribute1": self.attribute1,
            "attribute2": self.attribute2,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "starship_id": self.starship_id,
            "user": self.user.serialize(),
            "character": self.character.serialize() if self.character else None,
            "planet": self.planet.serialize() if self.planet else None,
            "starship": self.starship.serialize() if self.starship else None,
        }
