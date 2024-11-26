from flask import Flask, request, jsonify
from schemas import order_schema
from models import Order
from main import db
from marshmallow import ValidationError

# creating an order
@app.route('/orders', methods=['POST'])
def create_order()
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # if the proper information was input, it will create a user object    
    new_order = Order(order_date = order_data['order_date'])
    db.session.add(new_order)
    db.session.commit()
    # sending user object back to confirm new user was added to the database
    return order_schema.jsonify(new_order), 201 

#  Read all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()

    return orders_schema.jsonify(orders), 200

# Read one order by ID
@app.route('/orders/<int:id>', methods=['GET'])
def get_orders(id):
    user = db.session.get(Order, id)
    return order_schema.jsonify(order), 200

# Update an order
@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = db.session.get(Order, id)
    # Error if user not found
    if not order:
        return jsonify({"message": "Invalid user id"}), 400
    # If user found, new information will be updated
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    order.order_date = order_data['order_date']
    # commiting chnages and return the user object back as confirmation of the update
    db.session.commit()
    return order_schema.jsonify(order), 200

# Delete an order
@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = db.session.get(Order, id)
    # returning an error if user not found
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    # finding and deleting the user, then committing the change, also returning confirmation
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"succefully deleted order {id}"}), 200