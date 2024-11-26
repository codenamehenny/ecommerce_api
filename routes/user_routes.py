from flask import Flask, request, jsonify
from schemas import user_schema
from models import User
from main import db
from marshmallow import ValidationError

# defining the CRUD operations for User and creating endpoints
@app.route('/users', methods=['POST'])
def create_user()
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

#  Read all users 
@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()

    return users_schema.jsonify(users), 200

# Read one user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

# Update User
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
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
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    # returning an error if user not found
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    # finding and deleting the user, then committing the change, also returning confirmation
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"succefully deleted user {id}"}), 200