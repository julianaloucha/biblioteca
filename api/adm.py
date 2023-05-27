# api/users.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from settings import users_collection

adm_blueprint = Blueprint('adm', __name__)

# Enable CORS headers
@adm_blueprint.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response

# Criar um novo usuário
@adm_blueprint.route('/adm', methods=['POST'])
def create_user():
    user = request.get_json()
    user['password'] = generate_password_hash(user['password'])
    result = users_collection.insert_one(user)
    user['_id'] = str(result.inserted_id)
    return jsonify(user), 201

# Logar um usuário
@adm_blueprint.route('/loginadm', methods=['POST'])
def login_adm():
    user = request.get_json()
    db_user = users_collection.find_one({'email': user['email']})
    if db_user and check_password_hash(db_user['password'], user['password']):
        return jsonify({'result': 'Logged in successfully', 'user_id': str(db_user['_id'])}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

