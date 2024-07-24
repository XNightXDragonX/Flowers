from flask import abort
from flask_login import current_user

def admin_required(f): #проверка на администратора(в основном файле декоратор импортируется и защищает /graphql)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return f(*args, **kwargs)
        else:
            abort(403)
    wrap.__name__ = f.__name__
    return wrap