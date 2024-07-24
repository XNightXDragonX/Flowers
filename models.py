from flask_sqlalchemy import SQLAlchemy  # Импорт SQLAlchemy для работы с базой данных
from flask_bcrypt import Bcrypt  # Импорт Bcrypt для хэширования паролей
from flask_login import UserMixin, LoginManager  # Импорт UserMixin и LoginManager для управления пользователями

# Инициализация SQLAlchemy, Bcrypt и LoginManager
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Модель пользователя, наследующаяся от db.Model и UserMixin для интеграции с Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    username = db.Column(db.String(20), unique=True, nullable=False)  # Имя пользователя
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email пользователя
    password = db.Column(db.String(60), nullable=False)  # Хэшированный пароль пользователя
    role = db.Column(db.String(10), nullable=False, default='user')  # Роль пользователя, по умолчанию 'user'
    orders = db.relationship('Order', backref='user', lazy=True)  # Связь с моделью Order

    # Метод для представления объекта User в виде строки
    def __repr__(self):
        return f'<User {self.username}>'

# Модель заказа
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    name = db.Column(db.String(100), nullable=False)  # Имя получателя
    address = db.Column(db.String(200), nullable=False)  # Адрес доставки
    flower_type = db.Column(db.String(100), nullable=False)  # Тип цветов в заказе
    message = db.Column(db.String(500), nullable=True)  # Сообщение к заказу
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Внешний ключ для связи с моделью User

    # Метод для представления объекта Order в виде строки
    def __repr__(self):
        return f'<Order {self.id}>'

# Модель цветов
class Flower(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    name = db.Column(db.String(100), nullable=False)  # Название цветка
    image_url = db.Column(db.String(200), nullable=False)  # URL изображения цветка
    length = db.Column(db.Float, nullable=False)  # Длина цветка
    price = db.Column(db.Float, nullable=False)  # Цена цветка

    # Метод для представления объекта Flower в виде строки
    def __repr__(self):
        return f'<Flower {self.name}>'

# Функция для загрузки пользователя по ID, необходимая для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))