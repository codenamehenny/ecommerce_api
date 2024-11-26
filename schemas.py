# This file contains the schemas to serialize and deserialize the models
from marshmallow import Schema, ValidationError
from models import User, Order, Product
from main import ma

# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
# Order Schema
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
       
# Product Schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrdersSchema(many=True)
product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
