from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from note.db import db
from note.user.models import User
from note.user.views import blueprint as user_blueprint
from note.note.views import blueprint as note_blueprint
from note.api.views import blueprint as api_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    migrate = Migrate(app, db)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(note_blueprint)
    app.register_blueprint(api_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/api/v1/notes', methods=['POST'])
    def create_note():
        if not request.json or not 'name' in request.json:
            abort(400)
        note = Note(
            user_id=request.json["user_id"],
            type='note',
            name=request.json["name"],
            text=request.json.get('text', ""),
            creation_dt=datetime.now(),
            tags=request.json.get('tags', "")
        )
        db.session.add(note)
        db.session.commit()
        return '200'

    @app.route('/api/v1/notes', methods=['GET'])
    def api_get_notes():
        if not request.json:
            abort(400)
        user = request.json["user_id"]
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

    @app.route('/api/v1/notes/<int:note_id>', methods=['GET'])
    def get_note():
        if not request.json:
            abort(400)
        user = request.json["user_id"]
        id = request.json['note_id']
        for note in Note.query.filter(Note.user_id == user, Note.note_id == id).all():
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

    @app.route('/api/v1/notes/<int:note_id>', methods=['POST'])
    def change_note(note_id):
        if not request.json:
            abort(400)
        n = Note.query.filter(Note.note_id == note_id).all()
        if n.user_id == request.json['user_id']:
            note = Note(
                note_id=note_id,
                user_id=request.json["user_id"],
                type='note',
                name=request.json["name"],
                text=request.json.get('text', ""),
                tags=request.json.get('tags', "")
            )
            db.session.add(note)
            db.session.commit()
            return '200'
        abort(403)

    return app
