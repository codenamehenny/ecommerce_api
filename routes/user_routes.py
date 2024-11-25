from flask import Flask, request

# defining the CRUD operations for User and creating endpoints
@app.route('\users', methods['POST'])
def create_user()
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # if the proper information was input, it will create a user object    
    new_user = User(name=user_data['name'], email=user_data['email'], address=user_data['address'])
    db.session.add(new_user)
    db.session.commit()
    # sending user object back to confirm new user was added to the database
    return user_schema.jsonify(new_user), 201 



