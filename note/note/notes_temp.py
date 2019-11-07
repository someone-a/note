# это временный файл с тестовыми данными для отладки работы view_notes

note1 = {
    'note_id': 1,
    'user_id': 2,
    'type': 'note',
    'name': 'Тестовая заметка 1',
    'text': 'Текст заметки',
    'creation_dt': '01-11-2019',
    'tags': 'python'
}

note2 = {
    'note_id': 2,
    'user_id': 2,
    'type': 'note',
    'name': 'Тестовая заметка 2',
    'text': 'Текст заметки',
    'creation_dt': '01-11-2019',
    'tags': 'python'
}

note3 = {
    'note_id': 3,
    'user_id': 2,
    'type': 'note',
    'name': 'Тестовая заметка 3',
    'text': 'Текст заметки',
    'creation_dt': '01-11-2019',
    'tags': 'python'
}

notes_list = [note1, note2, note3]

notes = {'notes': notes_list}


def notes_list_func():
    # note_list_view = notes['notes']
    # return note_list_view
    return notes
