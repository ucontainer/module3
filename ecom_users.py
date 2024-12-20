from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from ecom import app, db, Users, user_schema,users_schema

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 404
    
    new_user = Users(name=user_data['name'], address=user_data['address'], email=user_data['email'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 200

@app.route('/users', methods=['GET'])
def get_users():
    query = select(Users)
    users = db.session.execute(query).scalars().all()
    
    return users_schema.jsonify(users), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(Users, id)
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(Users, id)
    if not user:
        return jsonify({"message":"Invalid user ID."}), 404
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 404
    
    user.name = user_data['name']
    user.address = user_data['address']
    user.email = user_data['email']
    
    db.session.commit()
    return user_schema.jsonify(user), 200    

@app.route('/users/<int:id>', methods= ['DELETE'])
def delete_user(id):
    user = db.session.get(Users, id)
    if not user:
        return jsonify({"message":"Invalid user ID."})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":f"Successfully deleted {user.name}."}), 200
    

app.run(debug=True)