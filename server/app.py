from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# Define a POST route to create a new BakedGood
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form  # Assuming form data is sent

    # Check if required fields are present in the form data
    if 'name' not in data or 'price' not in data or 'bakery_id' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    # Create a new BakedGood and add it to the database
    baked_good = BakedGood(
        name=data['name'],
        price=data['price'],
        bakery_id=data['bakery_id']
    )

    db.session.add(baked_good)
    db.session.commit()

    return jsonify({"message": "BakedGood created successfully", "data": baked_good.to_dict()}), 201

# Define a PATCH route to update the name of a Bakery
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    data = request.form  # Assuming form data is sent

    # Retrieve the bakery by ID
    bakery = Bakery.query.get(id)

    if bakery is None:
        return jsonify({"message": "Bakery not found"}), 404

    # Update the bakery name if it's provided in the form data
    if 'name' in data:
        bakery.name = data['name']

    db.session.commit()

    return jsonify({"message": "Bakery updated successfully", "data": bakery.to_dict()}), 200

# Define a DELETE route to delete a BakedGood
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if baked_good is None:
        return jsonify({"message": "BakedGood not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "BakedGood deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
