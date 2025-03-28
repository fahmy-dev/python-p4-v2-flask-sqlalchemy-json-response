# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return make_response(
        {'message': 'Welcome to the pet directory!'},
        200
    )


@app.route('/pets/<int:id>')
def get_pet_by_id(id):
    pet = Pet.query.filter_by(id=id).first()

    if not pet:
        return make_response(
            {"error": "Pet not found"}, 404
        )

    pet_dict = {
        'id': pet.id, 
        'name' : pet.name, 
        'species' : pet.species
    }
    return make_response(pet_dict, 200)

@app.route('/species/<string:species>')
def get_pets_by_species(species):
    pets = Pet.query.filter_by(species=species).all()

    if not pets:
        return make_response(
            {'error': f'No pets found of species {species}'}, 404
        )

    pets_list = []
    for pet in pets:
        pet_dict = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        pets_list.append(pet_dict)

    return make_response(
        {'pets': pets_list}, 200
    )

if __name__ == '__main__':
    app.run(port=5555, debug=True)
