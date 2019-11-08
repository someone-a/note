from note.user.forms import LoginForm, RegistrationForm
from note.user.models import User
from flask_login import current_user, login_user, logout_user
from flask import Blueprint, render_template, flash, redirect, url_for, request
import json
import requests

blueprint = Blueprint('user', __name__)


@blueprint.route('/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('note.create_note'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html',
                           page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('note.create_note'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('user.login'))


@blueprint.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('note.create_note'))
    title = 'Регистрация'
    registration_form = RegistrationForm()
    return render_template('user/registration.html',
                           page_title=title, form=registration_form)


@blueprint.route('/process-registration', methods=['POST'])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        dict_ = {'username': form.username.data,
                 'password': form.password.data,
                 'tg_login': form.tg_login.data}
        r = requests.post('http://'+request.host +
                          url_for('api.process_registration'),
                          json=json.dumps(dict_))
        if r.status_code == 200:
            flash('Успешная регистрация')
            return redirect(url_for('user.login'))

    flash('Ошибка регистрации')
    return redirect(url_for('user.registration'))
