from flask import Flask, render_template, url_for, flash, redirect, request, session
from config import Config
from models import db, bcrypt, login_manager, User, Order, Flower
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Создание таблиц при первом запуске
with app.app_context():
    db.create_all()

# Добавление некоторых цветов в базу данных при первом запуске
with app.app_context():
    if not Flower.query.first():
        flowers = [
            Flower(name='Роза', image_url='SHOP/static/images/rose.jpg', length=51, price=150),
            Flower(name='Тюльпан', image_url='SHOP/static/images/tulip.jpg', length=62, price=120),
            Flower(name='Лилия', image_url='SHOP/static/images/lily.jpg', length=56, price=180)
        ]
        db.session.bulk_save_objects(flowers)
        db.session.commit()

# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        flower_types = request.form.getlist('flower_type')
        message = request.form['message']
        
        new_order = Order(name=name, address=address, flower_type=','.join(flower_types), message=message, user_id=current_user.id)
        db.session.add(new_order)
        db.session.commit()
        
        session['order_created'] = True  # Установить переменную сессии для указания, что заказ был создан
        return redirect(url_for('index'))

    search_query = request.args.get('search', '')
    length_filter = request.args.get('length', '')
    price_filter = request.args.get('price', '')

    flowers = Flower.query.filter(Flower.name.contains(search_query))
    
    if length_filter:
        min_length, max_length = map(float, length_filter.split('-'))
        flowers = flowers.filter(Flower.length.between(min_length, max_length))
    if price_filter:
        min_price, max_price = map(float, price_filter.split('-'))
        flowers = flowers.filter(Flower.price.between(min_price, max_price))
    
    flowers = flowers.all()

    order_created = session.pop('order_created', False)  # Проверить и удалить переменную сессии
    return render_template('index.html', flowers=flowers, search_query=search_query, length_filter=length_filter, price_filter=price_filter, order_created=order_created)

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email_exists = User.query.filter_by(email=form.email.data).first()
        username_exists = User.query.filter_by(username=form.username.data).first()
        if email_exists:
            flash('Email уже зарегистрирован. Пожалуйста, используйте другой email.', 'danger')
        elif username_exists:
            flash('Имя пользователя уже занято. Пожалуйста, используйте другое имя пользователя.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Ваша учётная запись создана! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Неудачный вход. Пожалуйста, проверьте email и пароль.', 'danger')
    return render_template('login.html', form=form)

# Страница профиля
@app.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    order_numbers = {order.id: idx + 1 for idx, order in enumerate(orders)}
    return render_template('profile.html', user=current_user, orders=orders, order_numbers=order_numbers)

# Маршрут для выхода
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)