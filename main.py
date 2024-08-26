from flask import Flask, render_template, redirect, url_for, request, session, flash, current_app, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField,IntegerField, SelectField, TextAreaField, FieldList, FormField, EmailField, SubmitField, Form, HiddenField, DecimalField
from wtforms.validators import DataRequired, Email, Optional, EqualTo, Length
from functools import wraps
from random import sample
from sqlalchemy import func, inspect, or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, UserMixin, login_required, login_user, logout_user
import random
from datetime import datetime, timedelta
import logging
from flask_session import Session



logging.basicConfig(level=logging.DEBUG)

# Configuration class
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_BINDS = {
        'fillespanje': 'sqlite:///fillespanje.db',
        'flourocarbon': 'sqlite:///flourocarbon.db',
        'allround': 'sqlite:///allround.db',
        'surfcasting': 'sqlite:///surfcasting.db',
        'beach': 'sqlite:///beach.db',
        'spinning': 'sqlite:///spinning.db',
        'bolognese': 'sqlite:///bolognese.db',
        'jigg': 'sqlite:///jigg.db',
        'bolentino': 'sqlite:///bolentino.db',
        'makineta': 'sqlite:///makineta.db',
        'lures': 'sqlite:///lures.db',
        'grepa': 'sqlite:///grepa.db',
        'aksesore': 'sqlite:///aksesore.db',
        'oferta': 'sqlite:///oferta.db',
        'spearfishing': 'sqlite:///spearfishing.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask app and extensions setup
app = Flask(__name__)
# Initialize CSRF protection
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config.from_object(Config)
app.secret_key = 'deal23-1B'  # Needed for session management
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)



# Initialize SQLAlchemy
db = SQLAlchemy(app, session_options={"autoflush": False, "expire_on_commit": False})


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)
    orders = db.relationship('Orders', back_populates='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationFillespanje.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
class ProductVariationFlourocarbon(db.Model):
    __bind_key__ = 'flourocarbon'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('flourocarbon.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationFlourocarbon.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()



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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationAllround.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationSurfcasting.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationBeach.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationSpinning.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationBolognese.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationJigg.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationBolentino.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()
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
    @staticmethod
    def update_stock(product_id, quantity):
        variation = ProductVariationMakineta.query.filter_by(product_id=product_id).first()
        if variation:
            variation.stock -= quantity
            db.session.commit()

class Lures(db.Model):
    __bind_key__ = 'lures'
    __tablename__ = 'lures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    variations = db.relationship('ProductVariationLures', backref='lure', lazy=True)


class ProductVariationLures(db.Model):
    __bind_key__ = 'lures'
    __tablename__ = 'lures_variation'

    id = db.Column(db.Integer, primary_key=True)
    grams = db.Column(db.Integer, nullable=False)
    color_code = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    lure_id = db.Column(db.Integer, db.ForeignKey('lures.id'), nullable=False)

class Grepa(db.Model):
    __bind_key__ = "grepa"
    __tablename__ = "grepa"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))


class ProductVariationGrepa(db.Model):
    __bind_key__ = "grepa"
    __tablename__ = "grepa_variation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('grepa.id'), nullable=False)
    size = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)


    product = db.relationship('Grepa', backref=db.backref('variations', lazy=True))

class Aksesore(db.Model):
    __bind_key__ = "aksesore"
    __tablename__ = "aksesore"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationAksesore(db.Model):
    __bind_key__ = "aksesore"
    __tablename__ = "aksesore_variation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('aksesore.id'), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)


    product = db.relationship('Aksesore', backref=db.backref('variations', lazy=True))


class Oferta(db.Model):
    __bind_key__ = "oferta"
    __tablename__ = "oferta"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationOferta(db.Model):
    __bind_key__ = "oferta"
    __tablename__ = "oferta_variation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('oferta.id'), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    default_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)


    product = db.relationship('Oferta', backref=db.backref('variations', lazy=True))

class Spearfishing(db.Model):
    __bind_key__ = "spearfishing"
    __tablename__ = "spearfishing"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))

class ProductVariationSpearfishing(db.Model):
    __bind_key__ = "spearfishing"
    __tablename__ = "spearfishing_variation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('spearfishing.id'), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)


    product = db.relationship('Spearfishing', backref=db.backref('variations', lazy=True))


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
    categories = ['fillespanje', 'flourocarbon',  'allround', 'surfcasting', 'spinning', 'bolognese',
                  'jigg', 'bolentino', 'makineta']
    category_data = {}
    categories = {
        'Fillespanje': Fillespanje.query.all(),
        'Flourocarbon': Flourocarbon.query.all(),
        # 'All round': Allround.query.all(),
        'Surfcasting': Surfcasting.query.all(),
        'Spinning': Spinning.query.all(),
        'Bolognese': Bolognese.query.all(),
        'Jigg': Jigg.query.all(),
        # 'Bolentino': Bolentino.query.all(),
        'Makineta': Makineta.query.all()
    }

    # Select 4 random items for each category
    random_items = {}
    for category, items in categories.items():
        random_items[category] = random.sample(items, min(3 , len(items)))

    return render_template('index.html', categories=random_items)

@app.route('/aksesore')
def aksesore():
    products = db.session.query(Aksesore).all()
    for product in products:
        variations = db.session.query(ProductVariationAksesore).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("aksesore.html", products=products, variations=variations)


@app.route('/fillespanje')
def fillespanje():
    products = db.session.query(Fillespanje).all()
    for product in products:
        variations = db.session.query(ProductVariationFillespanje).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("fillespanje.html", products=products, variations=variations)

@app.route("/flourocarbon")
def flourocarbon():
    products = db.session.query(Flourocarbon).all()
    for product in products:
        variations = db.session.query(ProductVariationFlourocarbon).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("flourocarbon.html", products=products)


@app.route('/grepa')
def grepa():
    products = db.session.query(Grepa).all()
    for product in products:
        variations = db.session.query(ProductVariationGrepa).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("grepa.html", products=products, variations=variations)



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

@app.route('/lures')
def lures():
    products = Lures.query.all()
    return render_template('lures.html', products=products)

@app.route('/lure/<int:lure_id>')
def lure_details(lure_id):
    lure = Lures.query.get_or_404(lure_id)
    variations = ProductVariationLures.query.filter_by(lure_id=lure_id).all()

    # Group variations by grams
    variations_by_grams = {}
    max_stock = 0
    for variation in variations:
        grams = variation.grams
        if grams not in variations_by_grams:
            variations_by_grams[grams] = []
        variation_dict = {
            'id': variation.id,
            'img_url': variation.img_url,
            'color_code': variation.color_code,
            'price': variation.price,
            'stock': variation.stock
        }
        variations_by_grams[grams].append(variation_dict)
        # Update max_stock
        if variation.stock > max_stock:
            max_stock = variation.stock

    # Get the first image URL
    first_img = None
    for variations in variations_by_grams.values():
        if variations:
            first_img = variations[0]['img_url']
            break

    return render_template('lures_details.html', lure=lure, variations_by_grams=variations_by_grams, first_img=first_img, max_stock=max_stock, random_products=random_())

@app.route("/spearfishing")
def spearfishing():
    products = db.session.query(Spearfishing).all()
    for product in products:
        variations = db.session.query(ProductVariationSpearfishing).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)
    return render_template("spearfishing.html", products=products, variations=variations)


@app.route("/oferta")
def oferta():
    products = db.session.query(Oferta).all()

    # Iterate over each product to determine if it has stock and calculate price range
    for product in products:
        variations = db.session.query(ProductVariationOferta).filter_by(product_id=product.id).all()
        product.has_stock = any(v.stock > 0 for v in variations)

        if variations:
            # Extracting all sale prices from the variations
            prices = [v.sale_price for v in variations]
            product.min_price = min(prices)
            product.max_price = max(prices)
        else:
            product.min_price = product.max_price = None

    return render_template("oferta.html", products=products)


@app.route("/kontakto")
def kontakto():
    return render_template("kontakto.html")


product_models = {
    'fillespanje': (Fillespanje, ProductVariationFillespanje),
    'flourocarbon': (Flourocarbon, ProductVariationFlourocarbon),
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
def logout():
    logout_user()

    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

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

class ChangeOrderStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('shipped', 'Shipped')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')

# Admin dashboard route
@app.route('/admin')
@admin_required
def admin_dashboard():
    # Fetch total sales and ongoing orders
    form = ChangeOrderStatusForm()  # Create an instance of the form
    total_sales = int(db.session.query(db.func.sum(Orders.total_amount)).scalar() or 0)
    ongoing_orders = Orders.query.filter_by(status='ongoing').all()
    ongoing_orders_count = len(ongoing_orders)

    return render_template('dashboard.html',
                           total_sales=total_sales,
                           ongoing_orders_count=ongoing_orders_count,
                           orders=ongoing_orders,
                           form=form)



@app.route('/change_order_status/<int:order_id>', methods=['POST'])
def change_order_status(order_id):
    form = ChangeOrderStatusForm()
    if form.validate_on_submit():
        # Fetch the order and update its status
        order = Orders.query.get_or_404(order_id)
        order.status = form.status.data
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    else:
        flash('Error updating order status. Please try again.', 'danger')

    return redirect(url_for('admin_dashboard'))

def get_sales_count():
    # Implement logic to get the sales count
    # Example data:
    return Orders.query.filter_by(status='done').all()


def get_ongoing_orders():
    # Implement logic to get the list of ongoing orders
    # Example data:
    return Orders.query.filter_by(status='ongoing').all()

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


@app.route('/dashboard/add_product/<category>', methods=['GET', 'POST'])
def add_product(category):
    models = {
        'allround': (Allround, ProductVariationAllround),
        'surfcasting': (Surfcasting, ProductVariationSurfcasting),
        'beach': (Beach, ProductVariationBeach),
        'spinning': (Spinning, ProductVariationSpinning),
        'bolognese': (Bolognese, ProductVariationBolognese),
        'jigg': (Jigg, ProductVariationJigg),
        'bolentino': (Bolentino, ProductVariationBolentino)
    }

    if category not in models:
        flash('Invalid category.', 'danger')
        return redirect(url_for('admin_dashboard'))

    Model, VariationModel = models[category]

    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = Model(
            id=product_id,
            product_name=name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Handle variations
        variation_meters = request.form.getlist('variations[][meters]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')
        variation_actions = request.form.getlist('variations[][action]')

        num_variations = len(variation_meters)
        if (len(variation_prices) != num_variations or
                len(variation_stocks) != num_variations or
                len(variation_actions) != num_variations):
            flash('Mismatch in variation data lengths.', 'danger')
            return redirect(url_for('add_product', category=category))

        for i in range(num_variations):
            meters = variation_meters[i]
            price = variation_prices[i]
            stock = variation_stocks[i]
            action = variation_actions[i]
            variation = VariationModel(
                product_id=new_product.id,
                meters=meters,
                price=float(price),
                stock=int(stock),
                action=action
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_products.html', category=category)

@app.route('/dashboard/add_product_lures', methods=['GET', 'POST'])
def add_product_lures():
    if request.method == 'POST':
        product_name = request.form['product_name']

        description = request.form.get('description', '')

        # Create and add the main product without setting the id
        new_lure = Lures(
            name=product_name,
            description=description
        )
        db.session.add(new_lure)
        db.session.commit()

        # Handle variations
        variation_grams = request.form.getlist('variations[][grams]')
        variation_color_codes = request.form.getlist('variations[][color_code]')
        variation_img_urls = request.form.getlist('variations[][img_url]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')

        num_variations = len(variation_grams)
        if (len(variation_color_codes) != num_variations or
                len(variation_img_urls) != num_variations or
                len(variation_prices) != num_variations or
                len(variation_stocks) != num_variations):
            flash('Mismatch in variation data lengths.', 'danger')
            return redirect(url_for('add_product_lures'))

        for i in range(num_variations):
            grams = variation_grams[i]
            color_code = variation_color_codes[i]
            variation_img_url = variation_img_urls[i]
            price = variation_prices[i]
            stock = variation_stocks[i]
            variation = ProductVariationLures(
                lure_id=new_lure.id,
                grams=grams,
                color_code=color_code,
                img_url=variation_img_url,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Lure and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_lures.html')

# Grepa
@app.route('/dashboard/add_product_grepa', methods=['GET', 'POST'])
def add_product_grepa():
    if request.method == 'POST':
        product_name = request.form['product_name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')
        id = request.form['product_id']
        # Create and add the main product
        new_grepa = Grepa(
            id = id,
            product_name=product_name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_grepa)
        db.session.commit()

        # Handle variations
        variation_sizes = request.form.getlist('variations[][size]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')

        num_variations = len(variation_sizes)
        if (len(variation_prices) != num_variations or
                len(variation_stocks) != num_variations):
            flash('Mismatch in variation data lengths.', 'danger')
            return redirect(url_for('add_product_grepa'))

        for i in range(num_variations):
            size = variation_sizes[i]
            price = variation_prices[i]
            stock = variation_stocks[i]
            variation = ProductVariationGrepa(
                product_id=new_grepa.id,
                size=size,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Grepa and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_grepa.html')


# Aksesore
@app.route('/dashboard/add_product_aksesore', methods=['GET', 'POST'])
def add_product_aksesore():
    if request.method == 'POST':
        product_name = request.form['product_name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = Aksesore(
            product_name=product_name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Handle variations
        variation_types = request.form.getlist('variations[][type]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')

        for i in range(len(variation_types)):
            variation = ProductVariationAksesore(
                product_id=new_product.id,
                type=variation_types[i],
                price=float(variation_prices[i]),
                stock=int(variation_stocks[i])
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_aksesore.html', category='aksesore')

@app.route('/dashboard/add_product_oferta', methods=['GET', 'POST'])
def add_product_oferta():
    if request.method == 'POST':
        product_name = request.form['product_name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = Oferta(
            product_name=product_name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Handle variations
        variation_types = request.form.getlist('variations[][type]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_sale_price = request.form.getlist('variations[][sale_price]')
        variation_stocks = request.form.getlist('variations[][stock]')

        for i in range(len(variation_types)):
            variation = ProductVariationOferta(
                product_id=new_product.id,
                type=variation_types[i],
                default_price=float(variation_prices[i]),
                sale_price = float(variation_sale_price[i]),
                stock=int(variation_stocks[i])
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_oferta.html', category='oferta')

@app.route('/dashboard/add_product_spearfishing', methods=['GET', 'POST'])
def add_product_spearfishing():
    if request.method == 'POST':
        product_name = request.form['product_name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = Spearfishing(
            product_name=product_name,
            img_url=img_url,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Handle variations
        variation_types = request.form.getlist('variations[][type]')
        variation_prices = request.form.getlist('variations[][price]')
        variation_stocks = request.form.getlist('variations[][stock]')

        for i in range(len(variation_types)):
            variation = ProductVariationSpearfishing(
                product_id=new_product.id,
                type=variation_types[i],
                price=float(variation_prices[i]),
                stock=int(variation_stocks[i])
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_spearfishing.html', category='spearfishing')


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
    if product_type.lower() in ['spinning', 'allround', 'surfcasting', 'bolognese', 'jigg', 'bolentino']:
        relevant_fields = ['meters', 'action']
    elif product_type.lower() == 'makineta' or product_type.lower() == "reel":
        relevant_fields = ['size']
    elif product_type.lower() in ['fillespanje', 'filispanje', 'flourocarbon']:
        relevant_fields = ['diameter', 'meters']
    elif product_type.lower() == 'grepa':
        relevant_fields = ['size']
    elif product_type.lower() in ['aksesore', 'oferta', 'spearfishing'] :
        relevant_fields = ['type']
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

def get_variation_type(variation):
    # Automatically get relevant fields based on the variation object
    fields = inspect(variation).mapper.column_attrs.keys()
    # Build the 'type' string
    return ', '.join([f"{field}: {getattr(variation, field)}" for field in fields if getattr(variation, field)])


@app.route('/add_to_cart/<string:category>/<int:product_id>', methods=['POST'])
def add_to_cart(category, product_id):
    variation_id = request.form.get('variation_id')
    quantity = request.form.get('quantity', 1)

    if not variation_id:
        flash('Error: No variation selected')
        return redirect(url_for('product_details', category=category, product_id=product_id))

    # Retrieve or initialize the cart
    cart = session.get('cart', [])

    # Get the product and variation from the database
    product_model = globals().get(category.capitalize())
    variation_model = globals().get(f'ProductVariation{category.capitalize()}')

    if not product_model or not variation_model:
        return redirect(url_for('product_details', category=category, product_id=product_id))

    product = db.session.get(product_model, product_id)
    variation = db.session.get(variation_model, int(variation_id))

    if not product or not variation:
        return redirect(url_for('product_details', category=category, product_id=product_id))

    # Determine where to get the image URL
    img_url = variation.img_url if category.lower() == 'lures' else product.img_url
    price = variation.price if category.lower() != "oferta" else variation.sale_price

    # Add the product to the cart with the variation
    cart_item = {
        'category': category,
        'product_id': product_id,
        'variation_id': int(variation_id),
        'quantity': int(quantity),
        'price': price,
        'product_name': product.product_name if hasattr(product, 'product_name') else product.name,
        'img_url': img_url,
        'type': ', '.join([f"{field}: {getattr(variation, field)}" for field in get_relevant_fields(category)])
    }

    cart.append(cart_item)

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
    elif category in ['fillespanje', 'filispanje', 'flourocarbon']:
        return ['diameter', 'meters']
    elif category == 'lures':
        return ['grams', 'color_code']
    elif category == 'grepa':
        return ['size']
    elif category in ['aksesore', 'oferta', 'spearfishing']:
        return ['type']
    else:
        return []


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

        # Determine where to get the image URL
        img_url = variation.img_url if category.lower() == 'lures' else product.img_url
        price = variation.price if category.lower() != "oferta" else variation.sale_price

        # Build cart details
        cart_details.append({
            'category': category,
            'product_id': product_id,
            'variation_id': item['variation_id'],
            'img_url': img_url,
            'product_name': product.product_name if hasattr(product, 'product_name') else product.name,
            'quantity': quantity,
            'type': ', '.join([f"{field}: {getattr(variation, field)}" for field in get_relevant_fields(category)]),
            'price': price,
            'item_total_price': item_total_price
        })

    return render_template('cart.html', cart_details=cart_details, total_price=total_price)



@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    category = request.form.get('category')
    product_id = request.form.get('product_id')
    type = request.form.get('type')


    if not category or not product_id:
        flash('Invalid request')
        return redirect(url_for('cart'))

    # Get the cart from the session
    cart = session.get('cart', [])

    # Filter out the item to be removed
    cart = [item for item in cart if not (item['category'] == category and item['product_id'] == int(product_id) and item['type'] == type)]

    # Update the session
    session['cart'] = cart
    session.modified = True


    return redirect(url_for('cart'))

class CheckoutForm(FlaskForm):
    full_name = StringField('Emer Mbiemer', validators=[DataRequired()])
    phone_number = StringField('Nr. ', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    address = StringField('Adresa', validators=[DataRequired()], default="Shteti, Qyteti, Rruga")
    submit = SubmitField('Order')


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    # Relationship back to the User model
    user = db.relationship('User', back_populates='orders')

    # Relationship to OrderItem
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(255))  # Add this field for product image URL
    type = db.Column(db.String(255))  # Add this field for product type or other details

    # Relationship to Orders
    order = db.relationship('Orders', back_populates='items')

    def __repr__(self):
        return f'<OrderItem {self.id}>'


def calculate_total(cart_items):
    total = 0
    for item in cart_items:
        total += item['price'] * item['quantity']
    return total

def get_cart_items():
    cart = session.get('cart', [])
    # Transform cart session data to the required format if necessary
    return cart

@app.route('/order_summary/<int:order_id>')
@login_required
def order_summary(order_id):
    order = Orders.query.get(order_id)
    if order and order.user_id == current_user.id:
        return render_template('order_summary.html', order=order)
    return redirect(url_for('index'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        flash('You need to be logged in to access the checkout page.', 'warning')
        return redirect(url_for('login'))
    if get_cart_items() == []:
        return redirect(url_for('cart'))
    form = CheckoutForm()
    if form.validate_on_submit():
        # Collect form data
        full_name = form.full_name.data
        phone_number = form.phone_number.data
        email = form.email.data
        address = form.address.data

        # Calculate total amount
        cart_items = session.get('cart', [])
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)

        # Calculate earned points
        earned_points = total_amount // 100  # 1 point per 100 lek

        # Update user's points
        current_user.points += earned_points
        db.session.commit()  # Commit the points update

        # Create a new order
        order = Orders(
            customer_id=current_user.id,
            total_amount=total_amount,
            status='ongoing',
            email=email,
            phone_number=phone_number,
            address=address
        )
        db.session.add(order)
        db.session.commit()  # Commit to get the order ID

        # Add order items
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                product_name=item['product_name'],
                quantity=item['quantity'],
                price=item['price'],
                img_url=item['img_url'],
                type=item['type']
            )
            db.session.add(order_item)

        db.session.commit()

        # Clear the cart
        session.pop('cart', None)

        # Redirect to confirmation or order summary page
        flash(f'Thank you for your purchase! You earned {earned_points} points.', 'success')
        return redirect(url_for('index'))

    total_amount = calculate_total(session.get('cart', []))
    return render_template('checkout.html', form=form, total_amount=total_amount)



def calculate_total(cart_items):
    return sum(item['price'] * item['quantity'] for item in cart_items)


@app.route('/user')
def user():
    user = current_user
    orders = Orders.query.filter_by(customer_id=user.id).all()

    return render_template('user-dash.html', user=user, orders=orders)

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            a = 'iypq bhpq kqaj uwxo'
            # Implement password reset logic here (e.g., send email with reset link)
            flash('Password reset link has been sent to your email.', 'info')
        else:
            flash('No account found with that email address.', 'danger')

    return render_template('forgot_password.html', form=form)





class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('change_password'))

        if new_password != confirm_new_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password'))

        if len(new_password) < 8:
            flash('New password must be at least 8 characters long.', 'danger')
            return redirect(url_for('change_password'))

        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('user'))  # Redirect to the user dashboard

    return render_template('change_password.html', form=form)


def search_all_databases(query):
    product_models = [Fillespanje, Flourocarbon, Allround, Surfcasting,
                      Beach, Spinning, Bolognese, Jigg, Bolentino, Makineta, Aksesore, Lures, Grepa]

    results = []

    for model in product_models:
        if model.__tablename__ == 'lures':
            matching_items = model.query.filter(
                or_(
                    model.name.ilike(f"%{query}%"),
                    model.description.ilike(f"%{query}%")
                )
            ).all()
            for item in matching_items:
                results.append({
                    'product': item,
                    'product_type': 'lure'
                })
        else:
            matching_items = model.query.filter(
                or_(
                    model.product_name.ilike(f"%{query}%"),
                    model.description.ilike(f"%{query}%")
                )
            ).all()
            for item in matching_items:
                results.append({
                    'product': item,
                    'product_type': model.__tablename__
                })

    return results




@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return render_template('search_results.html', query=query, results=[], has_results=False)

    # Perform the search across all databases
    results = search_all_databases(query)

    # Determine if there are any results
    has_results = len(results) > 0

    return render_template('search_results.html', query=query, results=results, has_results=has_results)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
