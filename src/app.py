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
from models import db, User , Character, Planet , Starship, Character_fav , Planet_fav, Starship_fav
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






############################# METODO GET ###################################


###### USERS ######

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    resultados = list(map(lambda item: item.serialize(), users))
    
    if not users:
        return jsonify(message="No se han encontrado usuarios"), 404

    return jsonify(resultados), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user2(user_id):
    user = User.query.get(user_id)  

    if user is None:
        return jsonify(message="Usuario no encontrado"), 404

    return jsonify(user.serialize()), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_fav():
    
    users = User.query.all()
    
    user_favorites = []
    
    for user in users:
        user_favorites.append({
            "user_id": user.id,
            "username": user.username,
            "character_favorites": [character_fav.character.serialize() for character_fav in user.character_fav],
            "planet_favorites": [planet_fav.planet.serialize() for planet_fav in user.planet_fav]
        })
    
    return jsonify(user_favorites), 200


####### CHARACTERS #######

@app.route('/character', methods=['GET'])
def get_character():
    characters = Character.query.all() 
    resultados = list(map(lambda item: item.serialize(), characters))
    
    if not characters:
        return jsonify(message="No se han encontrado personajes"), 404

    return jsonify(resultados), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character2(character_id):
    character = Character.query.get(character_id)  

    if character is None:
        return jsonify(message="Personaje no encontrado"), 404

    return jsonify(character.serialize()), 200

@app.route('/character_fav', methods=['GET'])
def get_character_fav():
    characters_fav = Character_fav.query.all() 
    resultados = list(map(lambda item: item.serialize(), characters_fav))
    
    if not characters_fav:
        return jsonify(message="No se han encontrado personajes favoritos"), 404

    return jsonify(resultados), 200


####### PLANETS #######

@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all() 
    resultados = list(map(lambda item: item.serialize(), planets))
    
    if not planets:
        return jsonify(message="No se han encontrado planetas"), 404

    return jsonify(resultados), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet2(planet_id):
    planet = Planet.query.get(planet_id)  

    if planet is None:
        return jsonify(message="Planeta no encontrado"), 404

    return jsonify(planet.serialize()), 200


@app.route('/planet_fav', methods=['GET'])
def get_planet_fav():
    planets_fav = Planet_fav.query.all() 
    resultados = list(map(lambda item: item.serialize(), planets_fav))
    
    if not planets_fav:
        return jsonify(message="No se han encontrado planetas favoritos"), 404

    return jsonify(resultados), 200


####### STARSHIPS #######

@app.route('/starship', methods=['GET'])
def get_starship():
    starships = Planet.query.all() 
    resultados = list(map(lambda item: item.serialize(), starships))
    
    if not starships:
        return jsonify(message="No se han encontrado naves"), 404

    return jsonify(resultados), 200

@app.route('/starship/<int:starship_id>', methods=['GET'])
def get_starship2(starship_id):
    starship = Starship.query.get(starship_id)  

    if starship is None:
        return jsonify(message="Nave no encontrada"), 404

    return jsonify(starship.serialize()), 200

@app.route('/starship_fav', methods=['GET'])
def get_starship_fav():
    starships_fav = Starship_fav.query.all() 
    resultados = list(map(lambda item: item.serialize(), starships_fav))
    
    if not starships_fav:
        return jsonify(message="No se han encontrado naves favoritas"), 404

    return jsonify(resultados), 200



############################# METODO POST ###################################


###### USERS ######

@app.route('/user', methods=['POST'])
def add_new_user():
    request_body_user = request.get_json()

   
    if (
        "email" not in request_body_user
        or "password" not in request_body_user
        or "username" not in request_body_user
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    new_user = User(
        username=request_body_user["username"],
        email=request_body_user["email"],
        password=request_body_user["password"],
        is_active=request_body_user["is_active"]
    )

    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "Nuevo usuario añadido correctamente"
    }

    return jsonify(response_body), 200


###### CHARACTERS ######

@app.route('/character', methods=['POST'])
def add_new_character():
    body = request.get_json()

    if (
        "name" not in body
        or "height" not in body
        or "mass" not in body
        or "hair_color" not in body
        or "skin_color" not in body
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    new_character = Character(
        name=body["name"],
        height=body["height"],
        mass=body["mass"],
        hair_color=body["hair_color"],
        skin_color=body["skin_color"]
    )

    db.session.add(new_character)
    db.session.commit()

    response_body = {
        "msg": "Nuevo personaje añadido correctamente"
    }

    return jsonify(response_body), 200

@app.route('/character_fav', methods=['POST'])
def add_new_character_fav():
    request_body_fav_character = request.get_json()


    if (
        "character_id" not in request_body_fav_character
        or "user_id" not in request_body_fav_character
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    
    new_fav_character = Character_fav(
        character_id=request_body_fav_character["character_id"],
        user_id=request_body_fav_character["user_id"]
    )
    
   
    db.session.add(new_fav_character)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character_fav añadido exitosamente"
    }

    return jsonify(response_body), 200


###### PLANETS ######

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

@app.route('/planet_fav', methods=['POST'])
def add_new_planet_fav():
    request_body_fav_planet = request.get_json()


    if (
        "planet_id" not in request_body_fav_planet
        or "user_id" not in request_body_fav_planet
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    
    new_fav_planet = Planet_fav(
        planet_id=request_body_fav_planet["planet_id"],
        user_id=request_body_fav_planet["user_id"]
    )
    
   
    db.session.add(new_fav_planet)
    db.session.commit()

    response_body = {
        "msg": "Nuevo planet_fav añadido exitosamente"
    }

    return jsonify(response_body), 200

###### STARSHIPS ######

@app.route('/starship', methods=['POST'])
def add_new_starship():
    body = request.get_json()
    
    if (
        "name" not in body
        or "model" not in body
        or "manufacturer" not in body
        or "cost_in_credits" not in body
        or "length" not in body
        or "crew" not in body
        or "passengers" not in body
        or "cargo_capacity" not in body
    ):
        return jsonify({"error": "Datos incompletos"}), 400
   
    new_starship = Starship(
        name=body["name"],
        model=body["model"],
        manufacturer=body["manufacturer"],
        cost_in_credits=body["cost_in_credits"],
        length=body["length"],
        crew=body["crew"],
        passengers=body["passengers"],
        cargo_capacity=body["cargo_capacity"],

    )
    
    db.session.add(new_starship)
    db.session.commit()

    response_body = {
        "msg": "Nueva nave añadida correctamente"
    }

    return jsonify(response_body), 200

@app.route('/starship_fav', methods=['POST'])
def add_new_starship_fav():
    request_body_fav_starship = request.get_json()


    if (
        "starship_id" not in request_body_fav_starship
        or "user_id" not in request_body_fav_starship
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    
    new_fav_starship = Starship_fav(
        starship_id=request_body_fav_starship["starship_id"],
        user_id=request_body_fav_starship["user_id"]
    )
    
   
    db.session.add(new_fav_starship)
    db.session.commit()

    response_body = {
        "msg": "Nueva nave favorita añadida correctamente"
    }

    return jsonify(response_body), 200


############################# METODO DELETE ###################################


###### USERS ######

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'Usuario con id {user_id} ha sido borrado'}), 200


###### PLANETS ######

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({'message': "Planeta no encontrado"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({'message': f'Planeta con id {planet_id} ha sido borrado'}), 200

@app.route('/planet_fav/<int:planet_fav_id>', methods=['DELETE'])
def delete_planet_fav(planet_fav_id):
    planet_fav = Planet_fav.query.get(planet_fav_id)

    if not planet_fav:
        return jsonify({'message': "Planeta favorito no encontrado"}), 404

    db.session.delete(planet_fav)
    db.session.commit()

    return jsonify({'message': f'Planeta favorito con ID {planet_fav_id} ha sido borrado'}), 200


####### CHARACTERS #######

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)

    if not character:
        return jsonify({'message': "Personaje no encontrado"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({'message': f'Personaje con id {character_id} ha sido borrado'}), 200

@app.route('/character_fav/<int:character_fav_id>', methods=['DELETE'])
def delete_character_fav(character_fav_id):
    character_fav = Character_fav.query.get(character_fav_id)

    if not character_fav:
        return jsonify({'message': "Entrada de Character_fav no encontrada"}), 404

    db.session.delete(character_fav)
    db.session.commit()

    return jsonify({'message': f'Personaje favorito con ID {character_fav_id} ha sido borrado'}), 200


####### STARSHIPS #######

@app.route('/starship/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    starship = Starship.query.get(starship_id)

    if not starship:
        return jsonify({'message': "Personaje no encontrado"}), 404

    db.session.delete(starship)
    db.session.commit()

    return jsonify({'message': f'Nave con id {starship_id} ha sido borrada'}), 200

@app.route('/starship_fav/<int:starship_fav_id>', methods=['DELETE'])
def delete_starship_fav(starship_fav_id):
    starship_fav = Starship_fav.query.get(starship_fav_id)

    if not starship_fav:
        return jsonify({'message': "Entrada de starship_fav no encontrada"}), 404

    db.session.delete(starship_fav)
    db.session.commit()

    return jsonify({'message': f'Personaje favorito con ID {starship_fav_id} ha sido borrado'}), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)