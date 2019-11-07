from note.db import db


class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=True)
    creation_dt = db.Column(db.DateTime, nullable=False)
    tags = db.Column(db.String, nullable=True)
