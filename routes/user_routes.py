from flask import Blueprint, request, jsonify
from schemas import user_schema, users_schema
from models import User
from app import db
from marshmallow import ValidationError
import sqlalchemy.orm import select

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