import json
import requests

from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user

from note.note.forms import CreateNoteForm
from note.note.notes_temp import notes_list_func # временно, эмуляция получения данных из api

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

    user_id_to_json = json.dumps({'user_id': current_user.id})
    try:
        all_user_notes = json.loads(requests.get('http://' + request.host + '/api/v1/notes', json=user_id_to_json)) # проверить, добавить url_for('api.api_get_notes')
        notes_list = all_user_notes['notes']
        print(all_user_notes)
    except (TypeError):
        flash('Сервис заметок временно недоступен')

    notes_list = notes_list_func()['notes'] # временно, эмуляция получения данных из api

    return render_template('note/view_notes.html', page_title = title, notes_list = notes_list)
