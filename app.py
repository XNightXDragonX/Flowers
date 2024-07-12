from flask import Flask, render_template, url_for, flash, redirect, request
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
            Flower(name='Роза', image_url='url_to_rose_image', length='50-56см', price=150),
            Flower(name='Тюльпан', image_url='url_to_tulip_image', length='57-60см', price=120),
            Flower(name='Лилия', image_url='url_to_lily_image', length='50-56см', price=180)
        ]
        db.session.bulk_save_objects(flowers)
        db.session.commit()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница оформления заказа
@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        flower_type = request.form['flower_type']
        message = request.form['message']
        
        new_order = Order(name=name, address=address, flower_type=flower_type, message=message)
        db.session.add(new_order)
        db.session.commit()
        
        return redirect(url_for('index'))

    search_query = request.args.get('search', '')
    length_filter = request.args.get('length', '')
    price_filter = request.args.get('price', '')

    flowers = Flower.query.filter(Flower.name.contains(search_query))
    
    if length_filter:
        flowers = flowers.filter_by(length=length_filter)
    if price_filter:
        min_price, max_price = map(float, price_filter.split('-'))
        flowers = flowers.filter(Flower.price.between(min_price, max_price))
    
    flowers = flowers.all()
    return render_template('order.html', flowers=flowers, search_query=search_query, length_filter=length_filter, price_filter=price_filter)

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
            flash('Email is already registered. Please use a different email.', 'danger')
        elif username_exists:
            flash('Username is already taken. Please use a different username.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
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
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)