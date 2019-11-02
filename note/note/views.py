from flask import Blueprint, render_template, flash, redirect, url_for
from note.note.forms import CreateNoteForm
from flask_login import current_user
import json

blueprint = Blueprint('note', __name__, url_prefix='/notes')


@blueprint.route('/create_note')
def create_note():
    if not current_user.is_authenticated:
        flash('log in first')
        return redirect(url_for('user.login'))
    title = 'Create note'
    create_note_form = CreateNoteForm()
    return render_template('note/create_note.html',
                           page_title=title,
                           form=create_note_form)


@blueprint.route('/note_to_db', methods=['POST'])
def note_to_db():
    form = CreateNoteForm()
    dict_ = {
        'id': current_user.id,
        'note_name': form.notename.data,
        'note_body': form.notebody.data
    }

    flash(f'json {json.dumps(dict_)}')
    return redirect(url_for('note.create_note'))

@blueprint.route('/view_notes')
def view_notes():
    if not current_user.is_authenticated:
        flash('log in first')
        return redirect(url_for('user.login'))
    title = 'View notes'
    return render_template('note/view_notes.html', page_title = title)
