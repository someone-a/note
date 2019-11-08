from telegram.ext import Updater, CommandHandler
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


def main(token):
    bot = Updater(token=token, request_kwargs=PROXY)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler("get_notes", get_notes))
    bot.start_polling()
    bot.idle()
