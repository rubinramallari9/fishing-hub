from flask import Flask, render_template, redirect, url_for, request, session, flash, current_app, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField,IntegerField, SelectField, TextAreaField, FieldList, FormField, EmailField, SubmitField, Form, HiddenField, DecimalField
from wtforms.validators import DataRequired, Email, Optional, EqualTo
from functools import wraps
from random import sample
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, UserMixin, login_required, login_user, logout_user
import random

# Configuration class
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_BINDS = {
        'fillespanje': 'sqlite:///fillespanje.db',
        'flourocarbon': 'sqlite:///flourocarbon.db',
        'shockleader': 'sqlite:///shockleader.db',
        'allround': 'sqlite:///allround.db',
        'surfcasting': 'sqlite:///surfcasting.db',
        'beach': 'sqlite:///beach.db',
        'spinning': 'sqlite:///spinning.db',
        'bolognese': 'sqlite:///bolognese.db',
        'jigg': 'sqlite:///jigg.db',
        'bolentino': 'sqlite:///bolentino.db',
        'makineta': 'sqlite:///makineta.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask app and extensions setup
app = Flask(__name__)
# Initialize CSRF protection
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config.from_object(Config)
app.secret_key = 'deal23-1B'  # Needed for session management
login_manager = LoginManager()
login_manager.init_app(app)




# Initialize SQLAlchemy
db = SQLAlchemy(app, session_options={"autoflush": False, "expire_on_commit": False})


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Fillespanje(db.Model):
    __bind_key__ = 'fillespanje'
    __tablename__ = 'fillespanje'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class Flourocarbon(db.Model):
    __bind_key__ = 'flourocarbon'
    __tablename__ = 'flourocarbon'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationFillespanje(db.Model):
    __bind_key__ = 'fillespanje'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('fillespanje.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

class ProductVariationFlourocarbon(db.Model):
    __bind_key__ = 'flourocarbon'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('flourocarbon.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

class Shockleader(db.Model):
    __bind_key__ = 'shockleader'
    __tablename__ = 'shockleader'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationShockleader(db.Model):
    __bind_key__ = 'shockleader'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('shockleader.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

class Allround(db.Model):
    __bind_key__ = 'allround'
    __tablename__ = 'allround'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationAllround(db.Model):
    __bind_key__ = 'allround'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('allround.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)

    product = db.relationship('Allround', backref=db.backref('variations', lazy=True))

class Surfcasting(db.Model):
    __bind_key__ = 'surfcasting'
    __tablename__ = 'surfcasting'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationSurfcasting(db.Model):
    __bind_key__ = 'surfcasting'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('surfcasting.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)

    product = db.relationship('Surfcasting', backref=db.backref('variations', lazy=True))

class Beach(db.Model):
    __bind_key__ = 'beach'
    __tablename__ = 'beach'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationBeach(db.Model):
    __bind_key__ = 'beach'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('beach.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)

    product = db.relationship('Beach', backref=db.backref('variations', lazy=True))

class Spinning(db.Model):
    __bind_key__ = 'spinning'
    __tablename__ = 'spinning'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationSpinning(db.Model):
    __bind_key__ = 'spinning'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('spinning.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)

    product = db.relationship('Spinning', backref=db.backref('variations', lazy=True))

class Bolognese(db.Model):
    __bind_key__ = 'bolognese'
    __tablename__ = 'bolognese'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationBolognese(db.Model):
    __bind_key__ = 'bolognese'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('bolognese.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)

    product = db.relationship('Bolognese', backref=db.backref('variations', lazy=True))

class Jigg(db.Model):
    __bind_key__ = 'jigg'
    __tablename__ = 'jigg'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationJigg(db.Model):
    __bind_key__ = 'jigg'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('jigg.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)

    product = db.relationship('Jigg', backref=db.backref('variations', lazy=True))

class Bolentino(db.Model):
    __bind_key__ = 'bolentino'
    __tablename__ = 'bolentino'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationBolentino(db.Model):
    __bind_key__ = 'bolentino'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('bolentino.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)

    product = db.relationship('Bolentino', backref=db.backref('variations', lazy=True))

class Makineta(db.Model):
    __bind_key__ = 'makineta'
    __tablename__ = 'makineta'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationMakineta(db.Model):
    __bind_key__ = 'makineta'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('makineta.id'), nullable=False)
    size = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship('Makineta', backref=db.backref('variations', lazy=True))
# Decorator to require login

# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Product form
class ProductForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    product_name = StringField('Product Name', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    size = StringField('Size', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    category = SelectField('Category', choices=[('fillespanje', 'Fillespanje'),
                                                 ('flourocarbon', 'Flourocarbon'),
                                                 ('shock_leader', 'Shock Leader'),
                                                 ('allround', 'All Round'),
                                                 ('surfcasting', 'Surfcasting'),
                                                 ('spinning', 'Spinning'),
                                                 ('bolognese', 'Bolognese'),
                                                 ('jigg', 'JIGG'),
                                                 ('bolentino', 'Bolentino'),
                                                 ('makineta', 'Makineta')])

# Index route
@app.route('/')
def index():
    categories = ['fillespanje', 'flourocarbon', 'shockleader', 'allround', 'surfcasting', 'spinning', 'bolognese',
                  'jigg', 'bolentino', 'makineta']
    category_data = {}
    categories = {
        'Fillespanje': Fillespanje.query.all(),
        'Flourocarbon': Flourocarbon.query.all(),
        # 'Shockleader': Shockleader.query.all(),
        # 'All round': Allround.query.all(),
        # 'Surfcasting': Surfcasting.query.all(),
        # 'Spinning': Spinning.query.all(),
        # 'Bolognese': Bolognese.query.all(),
        # 'Jigg': Jigg.query.all(),
        # 'Bolentino': Bolentino.query.all(),
        'Makineta': Makineta.query.all()
    }

    # Select 4 random items for each category
    random_items = {}
    for category, items in categories.items():
        random_items[category] = random.sample(items, min(3 , len(items)))

    return render_template('index.html', categories=random_items)

@app.route('/fillespanje')
def fillespanje():
    products = db.session.query(Fillespanje).all()
    for product in products:
        variations = db.session.query(ProductVariationFillespanje).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("fillespanje.html", products=products)

@app.route("/flourocarbon")
def flourocarbon():
    products = db.session.query(Flourocarbon).all()
    for product in products:
        variations = db.session.query(ProductVariationFlourocarbon).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("flourocarbon.html", products=products)

@app.route('/shockleader')
def shockleader():
    products = db.session.query(Shockleader).all()
    for product in products:
        variations = db.session.query(ProductVariationShockleader).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("shockleader.html", products=products)

@app.route('/allround')
def allround():
    products = db.session.query(Allround).all()
    for product in products:
        variations = db.session.query(ProductVariationAllround).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("allround.html", products=products)

@app.route('/surfcasting')
def surfcasting():
    products = db.session.query(Surfcasting).all()
    for product in products:
        variations = db.session.query(ProductVariationSurfcasting).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("surfcasting.html", products=products)

@app.route('/beach')
def beach():
    products = db.session.query(Beach).all()
    for product in products:
        variations = db.session.query(ProductVariationBeach).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("beach.html", products=products)

@app.route('/spinning')
def spinning():
    products = db.session.query(Spinning).all()
    for product in products:
        variations = db.session.query(ProductVariationSpinning).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    print(products)
    return render_template("spinning.html", products=products)

@app.route('/bolognese')
def bolognese():
    products = db.session.query(Bolognese).all()
    for product in products:
        variations = db.session.query(ProductVariationBolognese).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("bolognese.html", products=products)

@app.route('/jigg')
def jigg():
    products = db.session.query(Jigg).all()
    for product in products:
        variations = db.session.query(ProductVariationJigg).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("jigg.html", products=products)

@app.route('/bolentino')
def bolentino():
    products = db.session.query(Bolentino).all()
    for product in products:
        variations = db.session.query(ProductVariationBolentino).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("bolentino.html", products=products)
@app.route("/makineta")
def makineta():
    products = db.session.query(Makineta).all()
    for product in products:
        variations = db.session.query(ProductVariationMakineta).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("makineta.html", products=products)


@app.route("/kontakto")
def kontakto():
    return render_template("kontakto.html")


product_models = {
    'fillespanje': (Fillespanje, ProductVariationFillespanje),
    'flourocarbon': (Flourocarbon, ProductVariationFlourocarbon),
    'shockleader': (Shockleader, ProductVariationShockleader),
    'allround': (Allround, ProductVariationAllround),
    'surfcasting': (Surfcasting, ProductVariationSurfcasting),
    'beach': (Beach, ProductVariationBeach),
    'spinning': (Spinning, ProductVariationSpinning),
    'bolognese': (Bolognese, ProductVariationBolognese),
    'jigg': (Jigg, ProductVariationJigg),
    'bolentino': (Bolentino, ProductVariationBolentino),
    'reel': (Makineta, ProductVariationMakineta)
}
def get_price_range(variations):
    prices = [variation.price for variation in variations]
    if not prices:
        return ""
    min_price, max_price = min(prices), max(prices)
    return f"${min_price:.2f} - ${max_price:.2f}" if min_price != max_price else f"${min_price:.2f}"


def random_():
    all_categories = list(product_models.keys())
    chosen_categories = sample(all_categories, min(5, len(all_categories)))

    random_products = {}

    for category in chosen_categories:
        product_model, _ = product_models[category]
        product = db.session.query(product_model).order_by(func.random()).first()
        if product:
            random_products[category] = product
    return random_products
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_user():
    return dict(current_user=current_user)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
# Login route

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Assuming you have a LoginForm defined

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('index'))  # Redirect to a protected route or home
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords must match.', 'danger')
            return redirect(url_for('signup'))

        # Check password length
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('signup'))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email address already exists.', 'danger')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='scrypt')

        # Create the new user
        new_user = User(email=email, password=hashed_password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        login_user(new_user)

        flash('Account created successfully!', 'success')
        return redirect(url_for('index'))  # Redirect to a protected route or dashboard

    return render_template('signup.html', form=form)




def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# Admin dashboard route
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    # Admin dashboard content
    return render_template('dashboard.html')

@app.route('/dashboard/add_product/fillespanje', methods=['GET', 'POST'])
def add_product_fillespanje():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = Fillespanje(
            id=product_id,
            product_name=name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Handle variations
        variation_diameters = request.form.getlist('variations[][diameter]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')
        variation_meters = request.form.getlist('variations[][meters]')

        num_variations = len(variation_diameters)
        if (len(variation_prices) != num_variations or
            len(variation_stocks) != num_variations or
            len(variation_meters) != num_variations):
            flash('Mismatch in variation data lengths.', 'danger')
            return redirect(url_for('add_product_fillespanje'))

        for i in range(num_variations):
            diameter = variation_diameters[i]
            price = variation_prices[i]
            stock = variation_stocks[i]
            meters = variation_meters[i]
            variation = ProductVariationFillespanje(
                product_id=new_product.id,
                diameter=diameter,
                meters=meters,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_fillespanje.html')



@app.route('/dashboard/add_product/flourocarbon', methods=['GET', 'POST'])
def add_product_flourocarbon():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = Flourocarbon(
            id=product_id,
            product_name=name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Handle variations
        variation_diameters = request.form.getlist('variations[][diameter]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')
        variation_meters = request.form.getlist('variations[][meters]')


        for i in range(len(variation_diameters)):
            diameter = variation_diameters[i]
            meters = variation_meters[i]
            price = variation_prices[i]
            stock = variation_stocks[i]

            variation = ProductVariationFlourocarbon(
                product_id=new_product.id,
                diameter=diameter,
                meters=meters,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_flourocarbon.html')

@app.route('/dashboard/add_product/shockleader', methods=['GET', 'POST'])
def add_product_shockleader():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        print(f"Product ID: {product_id}, Name: {name}, Image URL: {img_url}, Description: {description}")

        variation_diameters = request.form.getlist('variations[][diameter]')
        variation_meters = request.form.getlist('variations[][meters]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')

        print(f"Variation Diameters: {variation_diameters}")
        print(f"Variation Meters: {variation_meters}")
        print(f"Variation Prices: {variation_prices}")
        print(f"Variation Stocks: {variation_stocks}")

        new_product = Shockleader(
            id=product_id,
            product_name=name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        for i in range(len(variation_diameters)):
            diameter = variation_diameters[i]
            meters = variation_meters[i]
            price = variation_prices[i]
            stock = variation_stocks[i]
            variation = ProductVariationShockleader(
                product_id=new_product.id,
                diameter=diameter,
                meters=meters,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_shockleader.html')



# Add product route
@app.route('/dashboard/add_product/makineta', methods=['GET', 'POST'])
def add_productMakineta():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = Makineta(
            id=product_id,
            product_name=name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Handle variations
        variation_sizes = request.form.getlist('variations[][size]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')

        for i in range(len(variation_sizes)):
            size = variation_sizes[i]
            price = variation_prices[i]
            stock = variation_stocks[i]

            variation = ProductVariationMakineta(
                product_id=new_product.id,
                size=size,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin-dashboard'))

    return render_template('add_products.html')


@app.route('/product/<string:product_type>/<int:product_id>')
def product_details(product_type, product_id):
    # Dynamically get the model based on product_type
    model = globals()[product_type.capitalize()]
    product = model.query.get_or_404(product_id)

    # Dynamically get the variation model
    variation_model = globals()[f'ProductVariation{product_type.capitalize()}']
    variations = variation_model.query.filter_by(product_id=product_id).all()

    # Determine relevant fields based on product type
    if product_type in ['spinning', 'allround', 'surfcasting', 'bolognese', 'jigg', 'bolentino']:
        relevant_fields = ['meters', 'action']
    elif product_type.lower() == 'makineta' or product_type.lower() == "reel":
        relevant_fields = ['size']
    elif product_type.lower() in ['fillespanje', 'filispanje']:
        relevant_fields = ['diameter', 'meters']
    else:
        relevant_fields = ['diameter']

    # Calculate the maximum stock value for progress bar
    max_stock = max(variation.stock for variation in variations) if variations else 0

    # Render the template with the necessary context
    return render_template('product_details.html',
                           product=product,
                           variations=variations,
                           product_type=product_type,
                           max_stock=max_stock,
                           relevant_fields=relevant_fields,
                           random_products=random_(),
                           category=product_type)





@app.route('/add_to_cart/<string:category>/<int:product_id>', methods=['POST'])
def add_to_cart(category, product_id):
    variation_id = request.form.get('variation_id')  # This should not be None
    if variation_id is None:
        flash('Error: No variation selected')
        return redirect(url_for('product_details', category=category, product_id=product_id))

    quantity = request.form.get('quantity', 1)

    # Retrieve or initialize the cart
    cart = session.get('cart', [])

    # Get the product and variation from the database
    product_model = globals()[category.capitalize()]
    variation_model = globals()[f'ProductVariation{category.capitalize()}']
    product = db.session.get(product_model, product_id)
    variation = db.session.get(variation_model, int(variation_id))

    # Add the product to the cart with the variation
    cart.append({
        'category': category,
        'product_id': product_id,
        'variation_id': int(variation_id),  # Ensure this is converted to int
        'quantity': int(quantity),
        'price': variation.price,
        'product_name': product.product_name,
        'img_url': product.img_url,
        'type': ', '.join([f"{field}: {getattr(variation, field)}" for field in get_relevant_fields(category)])
    })

    # Save the cart back to the session
    session['cart'] = cart
    session.modified = True

    flash('Product added to cart!')
    return redirect(url_for('cart'))



def get_relevant_fields(category):
    category = category.lower()
    if category in ['spinning', 'allround', 'surfcasting', 'bolognese', 'jigg', 'bolentino']:
        return ['meters', 'action']
    elif category == 'makineta':
        return ['size']
    elif category in ['fillespanje', 'filispanje']:
        return ['diameter', 'meters']
    else:
        return ['diameter']

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_details = []
    total_price = 0

    for item in cart_items:
        category = item['category']
        product_id = item['product_id']
        quantity = item['quantity']

        # Dynamically get the product and variation models
        model = globals().get(category.capitalize())
        variation_model = globals().get(f'ProductVariation{category.capitalize()}')

        # Fetch the product and variation using Session.get()
        product = db.session.get(model, product_id) if model else None
        variation = db.session.get(variation_model, item['variation_id']) if variation_model else None

        # Skip if product or variation is not found
        if not product or not variation:
            continue

        # Calculate item total price
        item_total_price = quantity * variation.price

        # Add to total cart price
        total_price += item_total_price

        # Build cart details with error handling
        try:
            cart_details.append({
                'category': category,
                'product_id': product_id,  # Ensure this key is present
                'variation_id': item['variation_id'],  # Ensure this key is present
                'img_url': product.img_url,
                'product_name': product.product_name,
                'quantity': quantity,
                'type': ', '.join([f"{field}: {getattr(variation, field)}" for field in get_relevant_fields(category)]),
                'price': variation.price,
                'item_total_price': item_total_price
            })
        except AttributeError as e:
            flash(f"Error processing item in cart: {e}")
            continue


    return render_template('cart.html', cart_details=cart_details, total_price=total_price)


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    category = request.form.get('category')
    product_id = request.form.get('product_id')

    print(f"Removing item from cart - Category: {category}, Product ID: {product_id}")

    if not category or not product_id:
        flash('Invalid request')
        return redirect(url_for('cart'))

    # Get the cart from the session
    cart = session.get('cart', [])

    # Filter out the item to be removed
    cart = [item for item in cart if not (item['category'] == category and item['product_id'] == int(product_id))]

    # Update the session
    session['cart'] = cart
    session.modified = True

    flash('Product removed from cart!')
    return redirect(url_for('cart'))

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Order')

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    flash_messages = get_flashed_messages()
    # Retrieve user details if logged in
    if current_user.is_authenticated:
        if not form.email.data:
            form.full_name.data = current_user.full_name
            form.email.data = current_user.email

    # Calculate total price
    cart_items = session.get('cart', [])
    total_price = 0
    for item in cart_items:
        category = item['category']
        product_id = item['product_id']
        variation_id = item['variation_id']
        quantity = item['quantity']

        # Dynamically get the product and variation models
        model = globals().get(category.capitalize())
        variation_model = globals().get(f'ProductVariation{category.capitalize()}')

        # Fetch the product and variation
        product = model.query.get(product_id) if model else None
        variation = variation_model.query.get(variation_id) if variation_model else None

        if product and variation:
            total_price += variation.price * quantity

    if form.validate_on_submit():
        # Process the order
        # (Here you would typically save order details to the database)

        flash('Order placed successfully!', 'success')
        session.pop('cart', None)  # Clear the cart
        return redirect(url_for('index'))

    # Display any flash messages
    flash_messages = get_flashed_messages(with_categories=True)

    return render_template('checkout.html', form=form, total_price=total_price, flash_messages=flash_messages)


if __name__ == '__main__':
    app.run(debug=True)