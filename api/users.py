# api/users.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from settings import users_collection
import json

users_blueprint = Blueprint('users', __name__)

# Criar um novo usuário
@users_blueprint.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    user['status'] = "waiting"
    user['password'] = generate_password_hash(user['password'])
    result = users_collection.insert_one(user)
    user['_id'] = str(result.inserted_id)
    return jsonify(user), 201

# Logar um usuário
@users_blueprint.route('/login', methods=['POST'])
def login_user():
    user = request.get_json()
    db_user = users_collection.find_one({'email': user['email']})
    if db_user and check_password_hash(db_user['password'], user['password']):
        return jsonify({'result': 'Logged in successfully', 'user_id': str(db_user['_id'])}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

# Obter todas as tarefas (R)
@users_blueprint.route('/allusers', methods=['GET'])
def get_Users():
    allUsers = users_collection.find({})
    users_list = [user for user in allUsers]
    serialized_users = json.loads(json.dumps(users_list, default=str))
    return jsonify(serialized_users), 200
