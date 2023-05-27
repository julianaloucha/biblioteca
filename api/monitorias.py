from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from settings import books_collection
import json

monitorias_blueprint = Blueprint('monitorias', __name__)

# Criar uma tarefa (C)
@monitorias_blueprint.route('/monitorias', methods=['POST'])
def create():
    monitoria = request.get_json()
    result = books_collection.insert_one(monitoria)
    monitoria['_id'] = str(result.inserted_id)
    return jsonify(monitoria), 201

# Obter todas as tarefas (R)
@monitorias_blueprint.route('/monitorias/<user_id>', methods=['GET'])
def get(user_id):
    monitorias = []
    for monitoria in books_collection.find({"user_id": user_id}):  # filtrando as tarefas baseado no usuário autenticado
        monitoria['_id'] = str(monitoria['_id'])
        monitorias.append(monitoria)
    return jsonify(monitorias), 200

# Obter todas as tarefas (R)
@monitorias_blueprint.route('/monitorias', methods=['GET'])
def get_all_monitorias():
    allMonitorias = books_collection.find({})
    monitorias_list = [monitoria for monitoria in allMonitorias]
    serialized_monitorias = json.loads(json.dumps(monitorias_list, default=str))
    return jsonify(serialized_monitorias), 200

# Atualizar uma tarefa (U)
@monitorias_blueprint.route('/monitorias/<monitoria_id>', methods=['PUT'])
def update(monitoria_id):
    updated = request.get_json()
    updated.pop('_id', None)  # Remove o campo '_id' se estiver presente
    books_collection.update_one({'_id': ObjectId(monitoria_id)}, {'$set': updated})
    return jsonify(updated), 200


# Deletar uma tarefa (D)
@monitorias_blueprint.route('/monitorias/<monitoria_id>', methods=['DELETE'])
def delete(monitoria_id):
    books_collection.delete_one({'_id': ObjectId(monitoria_id)})
    return jsonify({'result': 'Monitoria deleted'}), 200
