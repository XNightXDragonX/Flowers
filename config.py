import os  # Импорт модуля os для работы с путями и переменными окружения

# Получение абсолютного пути к директории, в которой находится данный файл
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Класс Config содержит конфигурационные настройки для приложения
class Config:
    # Секретный ключ для обеспечения безопасности сессий и форм
    SECRET_KEY = 'your_secret_key'
    
    # Настройка URI для подключения к базе данных SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    
    # Отключение отслеживания модификаций объектов SQLAlchemy для улучшения производительности
    SQLALCHEMY_TRACK_MODIFICATIONS = False