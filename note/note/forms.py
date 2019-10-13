from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateNoteForm(FlaskForm):
    notename = StringField('Note name',
                           validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    notebody = TextAreaField('Note body',
                             validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    submit = SubmitField('Create note',
                         render_kw={'class': 'btn btn-primary'})
