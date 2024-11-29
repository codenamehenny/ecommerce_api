from flask import Blueprint, request, jsonify
from schemas import product_schema, products_schema
from models import Product
from app import db
from marshmallow import ValidationError

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