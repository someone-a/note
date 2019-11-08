from note.user.models import User
from note.note.models import Note
from note.db import db
from datetime import datetime
from flask import Blueprint, request, abort, jsonify
import json

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/process-registration', methods=['POST'])
def process_registration():
    data = json.loads(request.json)

    new_user = User(username=data['username'], tg_login=data['tg_login'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return '200'


@blueprint.route('/v1/notes', methods=['POST'])
def create_note():
    data = json.loads(request.json)
    if not (data or 'name' in data):
        abort(400)
    note = Note(
        user_id=data["user_id"],
        type='note',
        name=data["name"],
        text=data.get('text', ""),
        creation_dt=datetime.now(),
        tags=data.get('tags', "")
    )
    db.session.add(note)
    db.session.commit()
    return '200'


@blueprint.route('/v1/notes', methods=['GET'])
def api_get_notes():
    if not request.json:
        abort(400)
    user = json.loads(request.json)["user_id"]
    notes_list = []
    for note in Note.query.filter(Note.user_id == user).all():
        single_note = {
            'note_id': note.note_id,
            'user_id': note.user_id,
            'type': note.type,
            'name': note.name,
            'text': note.text,
            'creation_dt': note.creation_dt,
            'tags': note.tags
        }
        notes_list.append(single_note)
    return jsonify({'notes': notes_list})


@blueprint.route('/v1/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    if not request.json:
        abort(400)
    user = json.loads(request.json)["user_id"]
    id = json.loads(request.json)["note_id"]
    for note in Note.query.filter(Note.user_id == user,
                                  Note.note_id == id).all():
        single_note = {
            'note_id': note.note_id,
            'user_id': note.user_id,
            'type': note.type,
            'name': note.name,
            'text': note.text,
            'creation_dt': note.creation_dt,
            'tags': note.tags
        }
    return jsonify(single_note)


@blueprint.route('/v1/notes/<int:note_id>', methods=['POST'])
def change_note(note_id):
    if not request.json:
        abort(400)
    data = json.loads(request.json)

    note = Note.query.filter_by(note_id=note_id).first()
 
    note.user_id=data["user_id"]
    note.name = data["name"]
    note.type='note'
    note.text=data.get('text', "")
    note.creation_dt=datetime.now()
    note.tags=data.get('tags', "")

    db.session.commit()
    return '200'
    
    #abort(403)


@blueprint.route('/v1/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    if not request.json:
        abort(400)
    n = Note.query.filter(Note.note_id == note_id).all()
    if n.user_id == request.json['user_id']:
        Note.query.filter_by(note_id=note_id).delete()
