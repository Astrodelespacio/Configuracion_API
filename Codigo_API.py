from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))
    price = db.Column(db.Float, nullable=False)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price} for item in items])

@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price})

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data.get('description', ''), price=data['price'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id}), 201

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data['name']
    item.description = data.get('description', item.description)
    item.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
