from flask import Flask, request, jsonify
from schemas import order_schema, orders_schema, product_schema, products_schema
from models import Order, Product, User
from app import db
from marshmallow import ValidationError
from models import User

# POST - creating an order
@app.route('/orders', methods=['POST'])
def create_order()
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
@app.route('/orders/user/<int:user_id>', methods=['GET'])
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
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['GET'])
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
@app.route('/orders/<int:order_id>/products', methods=['GET'])
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
@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(order_id):
    order = db.session.get(Order, order_id)
    # returning an error if user not found
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    # finding and deleting the user, then committing the change, also returning confirmation
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"succefully deleted order {order_id}"}), 200