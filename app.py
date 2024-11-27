from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from models import Base

# initiatializing Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:henny04031998@127.0.0.1:3306/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class = Base)
db.init_app(app)
ma = Marshmallow(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)