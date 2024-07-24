from flask_wtf import FlaskForm  # Импорт базового класса формы из Flask-WTF
from wtforms import StringField, PasswordField, SubmitField, BooleanField  # Импорт полей формы из WTForms
from wtforms.validators import DataRequired, Length, Email, EqualTo  # Импорт валидаторов для проверки полей

# Класс формы для регистрации пользователей
class RegistrationForm(FlaskForm):
    # Поле для ввода имени пользователя с валидацией на обязательное заполнение и длину от 2 до 20 символов
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    # Поле для ввода email с валидацией на обязательное заполнение и корректный формат email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Поле для ввода пароля с валидацией на обязательное заполнение
    password = PasswordField('Пароль', validators=[DataRequired()])
    # Поле для повторного ввода пароля с валидацией на совпадение с полем password
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    # Кнопка отправки формы
    submit = SubmitField('Зарегистрироваться')

# Класс формы для входа пользователей
class LoginForm(FlaskForm):
    # Поле для ввода email с валидацией на обязательное заполнение и корректный формат email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Поле для ввода пароля с валидацией на обязательное заполнение
    password = PasswordField('Пароль', validators=[DataRequired()])
    # Чекбокс для запоминания пользователя
    remember = BooleanField('Запомнить меня')
    # Кнопка отправки формы
    submit = SubmitField('Войти')