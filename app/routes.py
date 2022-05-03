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

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{planet_id} successfully deleted")

# @planets_bp.route("/<planet_id>", methods = ["GET"])
# def single_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return planet