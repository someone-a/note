from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from note.user.models import User
from note import create_app
import json
import requests
from flask import url_for

PROXY = {'proxy_url': 'socks5://t3.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}


def get_notes(bot, update):
    app = create_app()
    login = update.message.chat.username
    app.config["SERVER_NAME"]="127.0.0.1:5000"
    with app.app_context():
        user_id_to_json = json.dumps(
            {'user_id': User.query.filter(User.tg_login == login).first().id})
        if user_id_to_json:
            try:
                all_user_notes = requests.get(
                    url_for('api.api_get_notes'),
                    json=user_id_to_json).json()
                notes_list = all_user_notes['notes']
                update.message.reply_text(notes_list)
            except Exception as e:
                print(e)
                update.message.reply_text("Сервис недоступен")
            return None
        update.message.reply_text("Телеграм аккаунт не привязан")

def note_get_name(bot, update, user_data):
    name = update.message.text
    user_data["note_name"] = name
    update.message.reply_text("Введите текст заметки")
    return "text"

def note_get_text(bot, update,user_data):
    text = update.message.text
    user_data["note_text"] = text
    user_data_to_json = json.dumps(user_data)
    new_note_try = requests.post(url_for('api.create_note'),
                    json=user_data_to_json)
    if new_note_try.status_code == '200':#проверяем что заметка создана
        update.message.reply_text("Заметка создана")
    else:
        update.message.reply_text("Что-то пошло не так")
    return ConversationHandler.END

def create_note(bot, update, user_data):
    app = create_app()
    login = update.message.chat.username
    app.config["SERVER_NAME"]="127.0.0.1:5000"
    with app.app_context():
        user_id_to_json = json.dumps(
            {'user_id': User.query.filter(User.tg_login == login).first().id})
        if user_id_to_json:
            try:
                user_data['user_id']= User.query.filter(User.tg_login == login).first().id
                update.message.reply_text("Введите название заметки")
                return 'name'

            except Exception as e:
                print(e)
                update.message.reply_text("Сервис недоступен")
            return None
        update.message.reply_text("Телеграм аккаунт не привязан")

def answer(bot, update):
    update.message.reply_text("Не понимаю вас. Введите команду /get_notes или /create_note")

def main(token):
    bot = Updater(token=token, request_kwargs=PROXY)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler("get_notes", get_notes))
    note = ConversationHandler(entry_points=[CommandHandler("create_note", create_note)],
                               states={'name': [MessageHandler(Filters.text, note_get_name)],
                                       "text": [MessageHandler(Filters.text, note_get_text)], })
    dp.add_handler(note)
    dp.add_handler(MessageHandler(Filters.text, answer))
    bot.start_polling()
    bot.idle()
