from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from ecom import app, db, Orders, Products, product_schema, products_schema

@app.route('/products', methods=['POST'])
def create_products():
    try: 
        product_data = product_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 404
        
    new_product = Products(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"messages":f"Successfully added {new_product.product_name}"})

@app.route('/products/<int:id>', methods=['PUT'])
def update_products(id):
    product = db.session.get(Products, id)
    if not product:
        return jsonify({"messages":"Product ID does not exist"}), 404
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 404
    
    product.product_name = product_data['product_name']
    product.price = product_data['price']
    
    db.session.commit()
    return product_schema.jsonify(product), 200

@app.route('/products', methods=['GET'])
def get_all_products():
    query = select(Products)
    products = db.session.execute(query).scalars().all()
    return products_schema.jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    query = db.session.get(Products, product_id)
    return product_schema.jsonify(query), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_products(id):
    product = db.session.get(Products, id)
    if not product:
        return jsonify({"messages":"Invalid product ID"})
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message":f"Successfully deleted {product.product_name}"})
    

app.run(debug=True)
    
    
    