print("🚀 Starting app.py...")
print("1. Importing Flask...")

from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

print("2. Creating app...")
app = Flask(__name__)
CORS(app)

print("3. Setting config...")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("4. Creating database...")
db = SQLAlchemy(app)

print("5. Defining models...")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)


print("6. Creating tables...")

with app.app_context():
    db.create_all()
    print("7. Adding sample products...")

    if Product.query.count() == 0:
        sample_products = [
            Product(name="Product 1", price=29.99, description="Test Product 1"),
            Product(name="Product 2", price=39.99, description="Test Product 2"),
            Product(name="Product 3", price=49.99, description="Test Product 3"),
        ]
        db.session.add_all(sample_products)
        db.session.commit()
        print("8. Products added!")

print("9. Defining routes...")


@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing fields"}), 400
    user = User(email=data['email'], password=data['password'], username=data.get('username', 'user'))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully", "user_id": user.id}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.password == data.get('password'):
        return jsonify({"message": "Login successful", "user_id": user.id, "is_admin": user.is_admin}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({"products": [{"id": p.id, "name": p.name, "price": p.price, "description": p.description} for p in
                                 products]}), 200


@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'], description=data.get('description'))
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added", "product_id": product.id}), 201


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200


@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total = 0
    items = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            items.append(
                {"id": item.id, "product_name": product.name, "price": product.price, "quantity": item.quantity})
            total += product.price * item.quantity
    return jsonify({"items": items, "total": total}), 200


@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Added to cart"}), 200


@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    if not cart_item:
        return jsonify({"error": "Item not found"}), 404
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Removed from cart"}), 200


@app.route('/api/checkout/<int:user_id>', methods=['POST'])
def checkout(user_id):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Checkout successful"}), 200


print("10. Routes defined!")
print("✅ App ready to run!\n")

if __name__ == '__main__':
    print("🚀 Flask starting on http://127.0.0.1:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)