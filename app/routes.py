from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.planet import Planet



planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({"message" : f"'{planet_id}' is invalid. ID must be an integer"}), 400

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"message" : f"Could not find '{planet_id}'"}), 404

    return planet


@planets_bp.route('', methods=['POST'])
def create_planet():
    request_body = request.get_json()

    new_planet = Planet (
        description = request_body['description'],
        name = request_body['name'],
        distance_from_sun = request_body['distance_from_sun']
    )

    db.session.add(new_planet)
    db.session.commit()

    return {
        'id' : new_planet.id
    }, 201

@planets_bp.route('', methods=['GET'])
def get_all_planets():
    response = []
    planets = Planet.query.all()
    for planet in planets:
        response.append(
            {
                'id' : planet.id,
                'description' : planet.description,
                'name' : planet.name,
                'distance_from_sun' : planet.distance_from_sun
                
            }
        )
    return jsonify(response)

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return {
        "name" : planet.name,
        "description" : planet.description,
        "distance_from_sun" : planet.distance_from_sun
    }  

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.distance_from_sun = request_body["distance_from_sun"]

    db.session.commit()

    return make_response(f"Planet #{planet.id} successfully updated")



# class Planet:
#     def __init__(self, id, description, name, distance_from_sun):
#         self.id = id
#         self.description = description
#         self.name = name
#         self.distance_from_sun = distance_from_sun

# planets = [
#     Planet(1, "The smallest planet", "Mercury", 36000000),
#     Planet(2, "Spins in opposite direction, hottest", "Venus", 67000000),
#     Planet(3, "Only planet we know of that has life", "Earth", 93000000),
#     Planet(4, "Dusty cold desert world with thin atmosphere", "Mars", 142000000),
#     Planet(5, "The biggest planet", "Jupiter", 484000000),
#     Planet(6, "Has a complex system of icy rings", "Saturn", 886000000),
#     Planet(7, "Uniquely tilted", "Uranus", 1800000000),
#     Planet(8, "Whipped by supersonic winds", "Neptune", 2800000000),
# ]

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         return jsonify({"message" : f"'{planet_id}' is invalid. ID must be an integer"}), 400

#     for planet in planets:
#         if planet_id == planet.id:
#             return jsonify({
#         "id" : planet.id,
#         "name" : planet.name,
#         "description" : planet.description,
#         "distance from sun" : planet.distance_from_sun
#     })
    
#     return jsonify({"message" : f"'{planet_id}' does not exist"}), 404
    



# @planets_bp.route("", methods = ["GET"])
# def list_planets():
#     planets_response = []
#     for planet in planets:
#         planets_response.append({
#             "id" : planet.id,
#             "name" : planet.name,
#             "description" : planet.description,
#             "distance from sun" : planet.distance_from_sun
#         })
#     return jsonify(planets_response)

# @planets_bp.route("/<planet_id>", methods = ["GET"])
# def single_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return planet