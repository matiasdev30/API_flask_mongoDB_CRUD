from bson.objectid import ObjectId
from flask import Flask, request
from flask.json import jsonify
from flask.wrappers import Response
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
client = MongoClient(host='localhost', port=27017)


@app.route('/create_note', methods=['POST'])
def create_note():
    note = request.json['note']
    create_date = request.json['create_date']

    if note and create_date:
        id = client.note_db.notes.insert_one({
            'note': note,
            'create_date': create_date
        })

        response = jsonify({
            'id' : str(id),
            'note' : note,
            'create_date' : create_date
        })

        return response

    else :
        return not_foud()

@app.errorhandler(404)
def not_foud(error=None):
    response  = jsonify({
        'msg' : 'Requerimento invalido ' + request.url,
        'status' : 404
    })

    response.status_code = 404
    return response

@app.route('/get_notes', methods=['GET'])
def get_notes():
    notes = client.note_db.notes.find()
    response = json_util.dumps(notes)
    return Response(response, mimetype='/aplication/json')

@app.route('/get_note/<id>')
def get_note(id):
    note = client.note_db.notes.find_one({'_id' : ObjectId(id)})
    response = json_util.dumps(note)
    return Response(response, mimetype='/aplication/json')

@app.route('/delete_note/<id>', methods=['DELETE'])
def delete_note(id):
    note = client.note_db.notes.delete_one({'_id' : ObjectId(id)})
    return jsonify({'msg': 'Nota apagada'})

@app.route('/update_note/<id>', methods=["PUT"])
def update_note(id):
    note = request.json['note']
    create_date = request.json['create_date']

    if note and create_date:
        id = client.note_db.notes.update_one({'_id' : ObjectId(id)},{'$set' : {
            'note' : note,
            'create_date' : create_date
        }})

        response = jsonify({
            'id' : str(id),
            'note' : note,
            'create_date' : create_date
        })

        return response

    else:
        not_foud()

if __name__ == '__main__':
    app.run(debug=True)
