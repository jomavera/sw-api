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
from models import db, User
from models import People, Planet, FavoritesPeople, FavoritesPlanets

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/users', methods=['GET'])
def handle_users():

    try:
        all_users = User.query.all()
        all_users= list(map(lambda x: x.serialize(), all_users))

        return jsonify(all_users), 200
    except:
        response_body = {
                "msg": "Error"
            }
        return jsonify(response_body), 500

@app.route('/users/favorites', methods=['GET'])
def handle_users_favorites():

    try:
        id_user = int(request.args.get('id_user'))
        favorite_people = FavoritesPeople.query.filter_by(id_user=id_user)
        favorite_people = list(map(lambda x: x.serialize(), favorite_people))

        favorite_planets = FavoritesPlanets.query.filter_by(id_user=id_user)
        favorite_planets= list(map(lambda x: x.serialize(), favorite_planets))

        favorites = {
            'people' : favorite_people,
            'planets': favorite_planets,
        }

        return jsonify(favorites), 200
    except Exception as error:
        print(f"users/favorites/: {error}")
        response_body = {
                "msg": "Error"
            }
        return jsonify(response_body), 500


@app.route('/people', methods=['GET'])
def handle_people():
    try:
        all_people = People.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))

        return jsonify(all_people), 200
    except:
        response_body = {
                "msg": "Error"
            }
        return jsonify(response_body), 500

@app.route('/onepeople', methods=['GET'])
def handle_one_person():

    try:
        id_people = int(request.args.get('id_people'))
        person_data = People.query.filter_by(id=id_people)
        person_data = list(map(lambda x: x.serialize(), person_data))
        return jsonify(person_data), 200
    except:
        response_body = {
                "msg": "Error"
        }
        return jsonify(response_body), 500

@app.route('/planets', methods=['GET'])
def handle_planets():
    try:
        all_planets = Planet.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        return jsonify(all_planets), 200
    except:
        response_body = {
                "msg": "Error"
            }
        return jsonify(response_body), 500

@app.route('/oneplanets', methods=['GET'])
def handle_planet():

    try:
        id_planet = int(request.args.get('id_planet'))
        planet_data = Planet.query.filter_by(id=id_planet)
        planet_data = list(map(lambda x: x.serialize(), planet_data))
        return jsonify(planet_data), 200
    except:
        response_body = {
                "msg": "Error"
            }
        return jsonify(response_body), 500

@app.route('/favorite/planet', methods=['POST', 'DELETE'])
def add_delete_favorite_planet():

    id_user = int(request.args.get('id_user'))
    id_planet = int(request.args.get('id_planet'))
    try:
        if request.method == 'POST':
            favorite = FavoritesPlanets(
                id_planet=id_planet,
                id_user=id_user
            )
            db.session.add(favorite)
            db.session.commit()
            response_body = {
                "msg": "Successfully add favorite planet to user"
            }
            return jsonify(response_body), 200

        elif request.method == 'DELETE':
            favorite = FavoritesPlanets(
                id_planet=id_planet,
                id_user=id_user
            )
            db.session.delete(favorite)
            db.session.commit()
            response_body = {
                "msg": "Successfully delete favorite planet to user"
            }
            return jsonify(response_body), 200
    except Exception as e:
        print(e)
        response_body = {
                "msg": "Error"
            }
        return jsonify(response_body), 500

@app.route('/favorite/people', methods=['POST', 'DELETE'])
def add_delete_favorite_people():
    id_user = int(request.args.get('id_user'))
    id_people = int(request.args.get('id_people'))
    try:
        if request.method == 'POST':
            favorite = FavoritesPeople(
                id_people=id_people,
                id_user=id_user
            )
            db.session.add(favorite)
            db.session.commit()
            response_body = {
                "msg": "Successfully add favorite person to user"
            }
            return jsonify(response_body), 200
        elif request.method == 'DELETE':
            favorite = FavoritesPeople(
                id_people=id_people,
                id_user=id_user
            )
            db.session.delete(favorite)
            db.session.commit()
            response_body = {
                "msg": "Successfully delete favorite person to user"
            }
            return jsonify(response_body), 200
    except Exception as e:
        print(e)
        response_body = {
                "msg": "Error"
            }
        return jsonify(response_body), 500

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
