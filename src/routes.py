from flask import Flask, request, jsonify, Blueprint
from models import db, User, Character, Vehicle, Planet

api = Blueprint ("api", __name__)

# User

@api.route("/users", methods = ["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route("/users/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 400
    return jsonify(user.serialize()), 200

@api.route("/users", methods = ["POST"])
def create_user():
    data = request.get_json()
    if (not data.get("email") 
    or not data.get("password") 
    or not data.get("username")
    or not data.get("firstname") 
    or not data.get("lastname")):
        return jsonify({"msg": "Missing fields"}), 400
    
    new_user = User(
        email = data["email"],
        password = data["password"],
        username = data["username"],
        firstname = data["firstname"],
        lastname = data["lastname"]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200

# Planet

@api.route("planets", methods = ["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@api.route("/planets/<int:planet_id>", methods = ["GET"])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "planet not found"}), 400
    return jsonify(planet.serialize()), 200

@api.route("/planets", methods = ["POST"])
def create_planet():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"msg": "Missing name"}), 400
    
    new_planet = Planet(
        name = data["name"],
        image = data["image"],
       
    )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 200

# Vehicle

@api.route("/vehicles", methods = ["GET"])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200

@api.route("/vehicles/<int:vehicle_id>", methods = ["GET"])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"msg": "vehicle not found"}), 400
    return jsonify(vehicle.serialize()), 200

@api.route("/vehicles", methods = ["POST"])
def create_vehicle():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"msg": "Missing name"}), 400
    
    new_vehicle = Vehicle(
        name = data["name"],
        image = data["image"]
       
    )
    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(new_vehicle.serialize()), 200

# Character

@api.route("/characters", methods = ["GET"])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

@api.route("/characters/<int:character_id>", methods = ["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msg": "character not found"}), 400
    return jsonify(character.serialize()), 200

@api.route("/characters", methods = ["POST"])
def create_character():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"msg": "Missing name"}), 400
    
    new_character = Character(
        name = data["name"],
        image = data["image"],
        quote = data["quote"]
    )
    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 200

# Favorites

@api.route("/<int:user_id>/favorite/<int:character_id>", methods = ["POST"])
def add_favorite_character(user_id, character_id):
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
       return jsonify({"msg":"User or character not found"}), 400

    if character in user.favorite_character:
       return jsonify({"msg":"Character already in favorites"})
    
    user.favorite_character.append(character)
    db.session.commit()

    return jsonify(user.serialize()), 200



@api.route("/<int:user_id>/favorite/vehicle/<int:vehicle_id>", methods = ["POST"])
def add_favorite_vehicle(user_id, vehicle_id):
    user = db.session.get(User, user_id)
    vehicle = db.session.get(Vehicle, vehicle_id)

    if not user or not vehicle:
       return jsonify({"msg":"User or vehicle not found"}), 400

    if vehicle in user.favorite_vehicle:
       return jsonify({"msg":"vehicle already in favorites"})
    
    user.favorite_vehicle.append(vehicle)
    db.session.commit()

    return jsonify(user.serialize()), 200



@api.route("/<int:user_id>/favorite/planet/<int:planet_id>", methods = ["POST"])
def add_favorite_planet(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    if not user or not planet:
       return jsonify({"msg":"User or planet not found"}), 400

    if planet in user.favorite_planet:
       return jsonify({"msg":"planet already in favorites"})
    
    user.favorite_planet.append(planet)
    db.session.commit()

    return jsonify(user.serialize()), 200


@api.route("/<int:user_id>/favorite/<int:character_id>", methods = ["DELETE"])
def remove_favorite_character(user_id, character_id):
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
       return jsonify({"msg":"User or character not found"}), 400
    
    if character in user.favorite_character:
        user.favorite_character.remove(character)
        db.session.commit()
    return jsonify(user.serialize()), 200


@api.route("/<int:user_id>/favorite/vehicle/<int:vehicle_id>", methods = ["DELETE"])
def remove_favorite_vehicle(user_id, vehicle_id):
    user = db.session.get(User, user_id)
    vehicle = db.session.get(Vehicle, vehicle_id)

    if not user or not vehicle:
       return jsonify({"msg":"User or vehicle not found"}), 400
    
    if vehicle in user.favorite_vehicle:
        user.favorite_vehicle.remove(vehicle)
        db.session.commit()
    return jsonify(user.serialize()), 200


@api.route("/<int:user_id>/favorite/planet/<int:planet_id>", methods = ["DELETE"])
def remove_favorite_planet(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    if not user or not planet:
       return jsonify({"msg":"User or planet not found"}), 400
    
    if planet in user.favorite_planet:
        user.favorite_planet.remove(planet)
        db.session.commit()
    return jsonify(user.serialize()), 200