from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from note.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    tg_login = db.Column(db.String(64), index=True, unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User name={} id={}> tg_login={}'.format(self.username, self.id, self.tg_login)
