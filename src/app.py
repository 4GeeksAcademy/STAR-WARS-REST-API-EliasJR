"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Starship, FavoriteItem
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

################################################ GETS #########################################


@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all()
    users = list(map(lambda user: user.serialize(), all_users))

    return jsonify(users), 200

@app.route('/character', methods=['GET'])
def get_character():
    all_characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), all_characters))

    return jsonify(characters), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    all_planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), all_planets))

    return jsonify(planets), 200

@app.route('/starship', methods=['GET'])
def get_starship():
    all_starships = Starship.query.all()
    starships = list(map(lambda starship: starship.serialize(), all_starships))

    return jsonify(starships), 200

@app.route('/favoriteItem', methods=['GET'])
def get_favorite_item():
    all_favoriteItem= FavoriteItem.query.all()
    favoriteItems = list(map(lambda favoriteItem: favoriteItem.serialize(), all_favoriteItem))

    return jsonify(favoriteItems), 200


################################################ POST #########################################


@app.route('/user', methods=['POST'])
def add_new_user():
    request_body_user = request.get_json()

   
    if (
        "email" not in request_body_user
        or "name" not in request_body_user
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    new_user = User(
        name=request_body_user["name"],
        email=request_body_user["email"]
    )

    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "Nuevo user añadido exitosamente"
    }

    return jsonify(response_body), 200


@app.route('/character', methods=['POST'])
def add_new_character():
    body = request.get_json()
    # Verificar si los datos esperados están presentes para el personaje
    if (
        "name" not in body
        or "height" not in body
        or "mass" not in body
        or "hair_color" not in body
        or "skin_color" not in body
    ):
        return jsonify({"error": "Datos incompletos"}), 400
    # Crear el personaje con los datos recibidos
    new_character = Character(
        name=body["name"],
        height=body["height"],
        mass=body["mass"],
        hair_color=body["hair_color"],
        skin_color=body["skin_color"]
    )
    # Agregar y confirmar los cambios en la base de datos
    db.session.add(new_character)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character añadido exitosamente"
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['POST'])
def add_new_planet():
    body = request.get_json()
    
    if (
        "name" not in body
        or "population" not in body
        or "terrain" not in body
        or "climate" not in body
    ):
        return jsonify({"error": "Datos incompletos"}), 400
   
    new_planet = Planet(
        name=body["name"],
        population=body["population"],
        terrain=body["terrain"],
        climate=body["climate"]
    )
    
    db.session.add(new_planet)
    db.session.commit()

    response_body = {
        "msg": "Nuevo planet añadido exitosamente"
    }

    return jsonify(response_body), 200


@app.route('/starship', methods=['POST'])
def add_new_starship():
    body = request.get_json()
    
    if (
        "name" not in body
        or "model" not in body
        or "manufacturer" not in body
        or "cargo_capacity" not in body
    ):
        return jsonify({"error": "Datos incompletos"}), 400
   
    new_starship = Starship(
        name=body["name"],
        model=body["model"],
        manufacturer=body["manufacturer"],
        cargo_capacity=body["cargo_capacity"]
    )
    
    db.session.add(new_starship)
    db.session.commit()

    response_body = {
        "msg": "Nueva nave añadida exitosamente"
    }

    return jsonify(response_body), 200



################################################ DELETE #########################################



@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'Uario con id {user_id} ha sido borrado'}), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)

    if not character:
        return jsonify({'message': "Personaje no encontrado"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({'message': f'Personaje con id {character_id} ha sido borrado'}), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({'message': "User no encontrado"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({'message': f'planet con id {planet_id} ha sido borrado'}), 200

@app.route('/starship/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    starship = Starship.query.get(starship_id)

    if not starship:
        return jsonify({'message': "Nave espacial no encontrada"}), 404

    db.session.delete(starship)
    db.session.commit()

    return jsonify({'message': f'Nave espacial con id {starship_id} ha sido borrada'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
