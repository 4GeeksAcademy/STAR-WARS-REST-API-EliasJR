from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False) 
    favorites = db.relationship("FavoriteItem", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
        }
    
class Planet(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
        }
    
class Starship(db.Model):
    __tablename__ = "Starships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model  = db.Column(db.Integer, nullable=False)
    manufacturer  = db.Column(db.String(50), nullable=False)
    cargo_capacity = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Starship %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cargo_capacity": self.cargo_capacity,
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
    starship_id = db.Column(db.Integer, db.ForeignKey("Starships.id"))  # Nota el cambio aquí

    user = db.relationship("User", back_populates="favorites")
    character = db.relationship("Character")
    planet = db.relationship("Planet")
    starship = db.relationship("Starship")

    def __repr__(self):
        return '<FavoriteItem %r>' % self.id

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
