from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import Base, User, Order, Product
from schemas import user_schema, users_schema, order_schema, orders_schema, product_schema, products_schema
from sqlalchemy.orm import select
from marshmallow import ValidationError


# initiatializing Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:henny04031998@127.0.0.1:3306/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class = Base)
db.init_app(app)
ma = Marshmallow(app)

# Registering blueprints
app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(order_blueprint, url_prefix='/api')
app.register_blueprint(product_blueprint, url_prefix='/api')

# --- USER ROUTES ---
# user blueprint
user_blueprint = Blueprint('users', __name__)

# POST - create user route
@blueprint.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # if the proper information was input, it will create a user object    
    new_user = User(
        name=user_data['name'], 
        email=user_data['email'], 
        address=user_data['address']
    )
    db.session.add(new_user)
    db.session.commit()
    # sending user object back to confirm new user was added to the database
    return user_schema.jsonify(new_user), 201 

# GET - Read all users 
@user_blueprint.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200

# Read one user by ID
@user_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

# Update User
@user_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(User, id)
    # Error if user not found
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    # If user found, new information will be updated
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.name = user_data['name']
    user.email = user_data['email']
    # commiting chnages and return the user object back as confirmation of the update
    db.session.commit()
    return user_schema.jsonify(user), 200

# Delete User
@user_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.get(User, id)
    # returning an error if user not found
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    # finding and deleting the user, then committing the change, also returning confirmation
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"succefully deleted user {id}"}), 200 

    # --- ORDER ROUTES --
    # defining order blueprint
order_blueprint = Blueprint('orders', __name__)

# --- ORDER ROUTES --

# POST - creating an order
@order_blueprint.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # check if user exits
    user = db.session.get(User, order_data['user_id'])
    if not user:
        return jsonify({
            "error": f"User with ID {order_data['user_id']} not found.
            Please add the user."
            }), 404
    # if user is found and the required information was entered, it creates the order
    user_id = order_data['user_id']
    order_date = order_data['order_date']    
    new_order = Order(user_id = user_id, order_date = order_date)
    db.session.add(new_order)
    db.session.commit()
    # sending user object back to confirm new user was added to the database
    return order_schema.jsonify(new_order), 201 

# GET - Read all orders for a user
@order_blueprint.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_for_user(user_id):
    # checking if user exists and returning an error if not
    user = db.session.get(User, order_data['user_id'])
    if not user:
        return jsonify({
            "error": f"User with ID {order_data['user_id']} not found.
            Please add the user."
            }), 404
    # getting all orders for a user
    orders = db.session.get(Order, user_id).all()
    return orders_schema.jsonify(orders), 200

# GET - Add a product to an order (preventing duplicates)
@order_blueprint.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['GET'])
def add_product_to_order(order_id, product_id):
    # checking if order exists
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({
            "error": f"Order ID {order_id} not found.
            Please place a new order."
            }), 404
    # checking if product exists
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({
            "error": f"Product ID {order_id} not found.
            Please add the product first."
            }), 404
    # preventing duplicates
    if product in order.products:
        return jsonify({
            "error": f"Product ID {product_id} is
            already in Order ID {order_id}"}), 400
    # adding the product to the order and returning order object as confirmation
    order.products.append(product)
    db.session.commit()
    return order_schema.jsonify(order), 200

# GET - All products from an order
@order_blueprint.route('/orders/<int:order_id>/products', methods=['GET'])
def get_products_for_order(order_id):
    # returning error if order doesn't exist
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({
            "error": f"Order ID {order_id} not found."
            }), 404
    # Get all products for an order
    products = order.products
    return products_schema.jsonify(products), 200    

# DELETE - Delete an order
@order_blueprint.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(order_id):
    order = db.session.get(Order, order_id)
    # returning an error if user not found
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    # finding and deleting the user, then committing the change, also returning confirmation
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"succefully deleted order {order_id}"}), 200


 # --- PRODUCT ROUTES ---

 # defining product blueprint
product_blueprint = Blueprint('products', __name__)

# POST - Create product
@product_blueprint.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # adding new product and returning the object for confirmation
    new_product = Product(product_name = product_data['product_name'],
        price = product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

# GET - All products
@product_blueprint.route('/products/<int:id>', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    if not products:
        return jsonify({"error": "no products added"})
    return products_schema.jsonify(products)

# GET - one product
@product_blueprint.route('/products/<int:id>' methods=['GET'])
def get_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({
            "error": "product not found, please add it"
            }) 404
    return product_schema.jsonify(product)

# PUT - Update a product
@product_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({
            "error": "product not found, please add it"
            }) 404
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # updating product
    product.product_name = product_data['product_name']
    product.price = product_data['price']
    db.session.commit()
    return product_schema.jsonify(product)

#  DELETE - removed product id
@product_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({
            "error": "product not found"
            }) 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message":
        f"Product ID {product_id} deleted successfully"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)