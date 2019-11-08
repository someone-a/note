import json
import requests

from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user

from note.note.forms import CreateNoteForm

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
    if form.validate_on_submit():
        dict_ = {
            'user_id': current_user.id,
            'type': 'note',
            'name': form.notename.data,
            'text': form.notebody.data
        }
        r = requests.post('http://'+request.host +
                          url_for('api.create_note'),
                          json=json.dumps(dict_))
        if r.status_code == 200:
            flash('Заметка создана')
            return redirect(url_for('note.view_notes'))

    flash('Ошибка создания заметки')
    return redirect(url_for('note.view_notes'))


@blueprint.route('/view_notes')
def view_notes():
    if not current_user.is_authenticated:
        flash('log in first')
        return redirect(url_for('user.login'))
    title = 'View notes'
    user_id_to_json = json.dumps({'user_id': current_user.id})
    try:
        all_user_notes = requests.get('http://' + request.host +
                                      url_for('api.api_get_notes'),
                                      json=user_id_to_json).json()
        notes_list = all_user_notes['notes']
    except (TypeError):
        flash('Сервис заметок временно недоступен')

    return render_template('note/view_notes.html',
                           page_title=title, notes_list=notes_list)

@blueprint.route('/edit_note/<int:note_id>')
def edit_note(note_id):
    if not current_user.is_authenticated:
        flash('log in first')
        return redirect(url_for('user.login'))

    title = 'Edit note'
    create_note_form = CreateNoteForm()
    create_json = json.dumps({'user_id': current_user.id, 'note_id': note_id})
   
    note = requests.get('http://' + request.host + url_for('api.api_get_notes') + '/' + str(note_id), json=create_json).json()
    
    return render_template('note/edit_note.html', page_title = title, form=create_note_form, note=note)

@blueprint.route('/edit_note_to_db/<int:note_id>', methods=['POST'])
def edit_note_to_db(note_id):
    form = CreateNoteForm()
    if form.validate_on_submit():
        dict_ = {
            'note_id': note_id,
            'user_id': current_user.id,
            'type': 'note',
            'name': form.notename.data,
            'text': form.notebody.data
        }
        r = requests.post('http://'+request.host + url_for('api.create_note') + '/' + str(note_id), json=json.dumps(dict_))
        #r = requests.post('http://127.0.0.1:5000/api/v1/notes/1', json=json.dumps(dict_))
        if r.status_code == 200:
            flash('Заметка обновлена')
            return redirect(url_for('note.view_notes'))
    flash('Ошибка создания заметки')
    return redirect(url_for('note.view_notes'))
