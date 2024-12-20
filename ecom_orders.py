from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from ecom import app, db, Orders, Products, order_schema, orders_schema

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 404
    #Date format "order_date":"2024-12-18T15:30:00"
    new_order = Orders(order_date = order_data['order_date'])
    
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message":"Order successfully added"})

@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['GET'])
def add_product_to_order(order_id, product_id):
   order = db.session.get(Orders, order_id)
   product = db.session.get(Products, product_id)
   
   if not order:
       return jsonify({"message":"Invalid order ID"})
   if not product: 
       return jsonify({"message":"Invalid product ID"})
   
   order.products.append(product)
   db.session.commit()
   return jsonify({"messages":f"{product.product_name} as been added to order {order.order_id}"})

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = db.session.get(Orders, order_id)
    if not order:
        return jsonify({"message":"Invalid order ID."})
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message":f"Successfully deleted order {order.order_id}"})

@app.route('/orders', methods=['GET'])
def get_all_orders():
    order = select(Orders)
    ordering = db.session.execute(order).scalars().all()
    return orders_schema.jsonify(ordering), 200

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    try:
        query = db.session.get(Orders, id)
    except:
        return jsonify({"message":"Invalid order id"})
        
    return order_schema.jsonify(query), 200

@app.route('/orders/<int:order_id>/product', methods=['GET'])
def orders_products(order_id):
    order = db.session.get(Orders, order_id)
    if not order:
        return jsonify({"message":"Invalid trainer ID."}), 404
    
    product = [p.product_name for p in order.products]
    return jsonify({"message":f"Order {order.order_id}: {product}"}), 200
    
app.run(debug=True)