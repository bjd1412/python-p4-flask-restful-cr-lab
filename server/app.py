#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):

    def get(self):
        plants = []
        allPlants = Plant.query.all()
        for plant in allPlants:
            plant_dict = plant.to_dict()
            plants.append(plant_dict)
        return make_response(plants, 200)

    def post(self):
        data = request.get_json()
        newplants = Plant(name = data['name'], image = data['image'], price = data['price'])

        db.session.add(newplants)
        db.session.commit()

        plant_dict = newplants.to_dict()

        return make_response(plant_dict, 201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        plant_dict = plant.to_dict()

        return make_response(plant_dict, 200)
    
        
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
