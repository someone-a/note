from note.user.models import User
from note.db import db
from flask import Blueprint, request
import json

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/process-registration', methods=['POST'])
def process_registration():
    data = json.loads(request.json)

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return '200'
