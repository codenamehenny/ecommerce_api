from flask import Flask, request, jsonify
from schemas import product_schema
from models import Product
from main import db
from marshmallow import ValidationError
import sqlalchemy.orm import Session

# POST - Create product
@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # adding new product and returning the object for confirmation
    new_product = Product(product_name = product_data['product_name'],
        price = product_data['price'])
    db.session.add(new_product)
    sb.session.commit()
    return product_schema.jsonify(new_product), 201

# GET - All products
@app.route('/products/<int:id>', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    if not products:
        return jsonify({"error": "no products added"})
    return products_schema.jsonify(products)

# GET - one product
@app.route('/products/<int:id>' methods=['GET'])
def get_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({
            "error": "product not found, please add it"
            }) 404
    return product_schema.jsonify(product)

# PUT - Update a product
@app.route('/products/<int:id>', methods=['PUT'])
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
@app.route('/products/<int:id>', methods=['DELETE'])
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