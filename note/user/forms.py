from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    remember_me = BooleanField('Запомнить меня',
                               default=True,
                               render_kw={"class": "form-check-input"})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    tg_login = StringField('Телеграм логин',
                           validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={'class': 'form-control'})

    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), EqualTo('password')],
                              render_kw={'class': 'form-control'})

    submit = SubmitField('Регистрация', render_kw={'class': 'btn btn-primary'})
