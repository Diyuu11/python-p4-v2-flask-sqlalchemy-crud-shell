# server/app.py

from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db

# create a Flask application instance 
app = Flask(__name__)

# configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# Create routes for CRUD operations

@app.route('/pets', methods=['POST'])
def add_pet():
    data = request.get_json()
    new_pet = Pet(name=data['name'], species=data['species'])
    db.session.add(new_pet)
    db.session.commit()
    return jsonify({'message': 'Pet added', 'pet': {'id': new_pet.id, 'name': new_pet.name, 'species': new_pet.species}}), 201

@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([{'id': pet.id, 'name': pet.name, 'species': pet.species} for pet in pets]), 200

@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = Pet.query.get(id)
    if pet:
        return jsonify({'id': pet.id, 'name': pet.name, 'species': pet.species}), 200
    return jsonify({'message': 'Pet not found'}), 404

@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    pet = Pet.query.get(id)
    if pet:
        data = request.get_json()
        pet.name = data['name']
        pet.species = data['species']
        db.session.commit()
        return jsonify({'message': 'Pet updated', 'pet': {'id': pet.id, 'name': pet.name, 'species': pet.species}}), 200
    return jsonify({'message': 'Pet not found'}), 404

@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get(id)
    if pet:
        db.session.delete(pet)
        db.session.commit()
        return jsonify({'message': 'Pet deleted'}), 200
    return jsonify({'message': 'Pet not found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
