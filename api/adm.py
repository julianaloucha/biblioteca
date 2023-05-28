# api/users.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from settings import adm_collection

adm_blueprint = Blueprint('adm', __name__)

# Criar um novo usuário
@adm_blueprint.route('/adm', methods=['POST'])
def create_adm():
    adm = request.get_json()
    adm['password'] = generate_password_hash(adm['password'])
    result = adm_collection.insert_one(adm)
    adm['_id'] = str(result.inserted_id)
    return jsonify(adm), 201

# Logar um usuário
@adm_blueprint.route('/loginadm', methods=['POST'])
def login_adm():
    adm = request.get_json()
    db_adm = adm_collection.find_one({'email': adm['email']})
    if db_adm and check_password_hash(db_adm['password'], adm['password']):
        return jsonify({'result': 'Logged in successfully', 'user_id': str(db_adm['_id'])}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

