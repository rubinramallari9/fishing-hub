from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, SelectField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap4
from random import sample
from sqlalchemy import func



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
        'reel': 'sqlite:///reel.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
Bootstrap4(app)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'  # Needed for session management
db = SQLAlchemy(app, session_options={"autoflush": False, "expire_on_commit": False})

# Define your models here (User, Fillespanje, ProductVariation)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Define a model for the 'fillespanje' database
class Fillespanje(db.Model):
    __bind_key__ = 'fillespanje'
    __tablename__ = 'fillespanje'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)


class Flourocarbon(db.Model):
    __bind_key__ = 'flourocarbon'
    __tablename__ = 'flourocarbon'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariation(db.Model):
    __bind_key__ = 'fillespanje'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('fillespanje.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)  # Add stock column

class ProductVariationFlourocarbon(db.Model):
    __bind_key__ = 'flourocarbon'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('flourocarbon.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)  # Add stock column

class Shockleader(db.Model):
    __bind_key__ = 'shockleader'
    __tablename__ = 'shockleader'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationShockleader(db.Model):
    __bind_key__ = 'shockleader'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('shockleader.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)  # Updated as string
    meters = db.Column(db.String(250), nullable=False)  # Updated as string
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)  # Add stock column

class Allround(db.Model):
    __bind_key__ = 'allround'
    __tablename__ = 'allround'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationAllround(db.Model):
    __bind_key__ = 'allround'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('allround.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Allround', backref=db.backref('variations', lazy=True))
class Surfcasting(db.Model):
    __bind_key__ = 'surfcasting'
    __tablename__ = 'surfcasting'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationSurfcasting(db.Model):
    __bind_key__ = 'surfcasting'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('surfcasting.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Surfcasting', backref=db.backref('variations', lazy=True))
class Beach(db.Model):
    __bind_key__ = 'beach'
    __tablename__ = 'beach'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationBeach(db.Model):
    __bind_key__ = 'beach'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('beach.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Beach', backref=db.backref('variations', lazy=True))

class Spinning(db.Model):
    __bind_key__ = 'spinning'
    __tablename__ = 'spinning'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationSpinning(db.Model):
    __bind_key__ = 'spinning'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('spinning.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Spinning', backref=db.backref('variations', lazy=True))

class Bolognese(db.Model):
    __bind_key__ = 'bolognese'
    __tablename__ = 'bolognese'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationBolognese(db.Model):
    __bind_key__ = 'bolognese'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('bolognese.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Bolognese', backref=db.backref('variations', lazy=True))

class Jigg(db.Model):
    __bind_key__ = 'jigg'
    __tablename__ = 'jigg'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationJigg(db.Model):
    __bind_key__ = 'jigg'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('jigg.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Jigg', backref=db.backref('variations', lazy=True))
class Bolentino(db.Model):
    __bind_key__ = 'bolentino'
    __tablename__ = 'bolentino'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationBolentino(db.Model):
    __bind_key__ = 'bolentino'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('bolentino.id'), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    action = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Bolentino', backref=db.backref('variations', lazy=True))


class Makineta(db.Model):
    __bind_key__ = "reel"
    __tablename__ = "reel"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))
class ProductVariationMakineta(db.Model):
    __bind_key__ = 'reel'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure autoincrement is enabled
    product_id = db.Column(db.Integer, db.ForeignKey('reel.id'), nullable=False)

    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    size = db.Column(db.String(250), nullable=False)  # New column

    product = db.relationship('Makineta', backref=db.backref('variations', lazy=True))


product_models = {
    'fillespanje': (Fillespanje, ProductVariation),
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
    chosen_categories = sample(all_categories, min(4, len(all_categories)))

    random_products = {}

    for category in chosen_categories:
        product_model, _ = product_models[category]
        product = db.session.query(product_model).order_by(func.random()).first()
        if product:
            random_products[category] = product
    return random_products

@app.route('/')
def index():
    return render_template('index.html', random_products=random_())

@app.route('/fillespanje')
def fillespanje():
    products = db.session.query(Fillespanje).all()
    for product in products:
        variations = db.session.query(ProductVariation).filter_by(product_id=product.id).all()
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


@app.route('/product/<string:product_type>/<int:product_id>')
def product_details(product_type, product_id):
    product_models = {
        'fillespanje': (Fillespanje, ProductVariation),
        'flourocarbon': (Flourocarbon, ProductVariationFlourocarbon),
        'shockleader': (Shockleader, ProductVariationShockleader),
        'allround': (Allround, ProductVariationAllround),
        'surfcasting': (Surfcasting, ProductVariationSurfcasting),
        'beach': (Beach, ProductVariationBeach),
        'spinning': (Spinning, ProductVariationSpinning),
        'bolognese': (Bolognese, ProductVariationBolognese),
        'jigg': (Jigg, ProductVariationJigg),
        'bolentino': (Bolentino, ProductVariationBolentino),
        'makineta': (Makineta, ProductVariationMakineta)
    }
    if product_type not in product_models:
        return redirect(url_for('index'))  # Redirect to home if product_type is invalid

    product_model, variation_model = product_models[product_type]
    product = db.session.query(product_model).filter_by(id=product_id).first_or_404()
    variations = db.session.query(variation_model).filter_by(product_id=product.id).all()
    max_stock = max((variation.stock for variation in variations), default=1)

    variation_fields = {
        'diameter': 'Diameter',
        'meters': 'Meters',
        'action': 'Action',
        'size': 'Size'
    }

    # Determine the relevant fields based on the product type
    relevant_fields = []
    if hasattr(variation_model, 'diameter'):
        relevant_fields.append('diameter')
    if hasattr(variation_model, 'meters'):
        relevant_fields.append('meters')
    if hasattr(variation_model, 'action'):
        relevant_fields.append('action')
    if hasattr(variation_model, 'size'):
        relevant_fields.append('size')

    return render_template("product_details.html", product=product, variations=variations, product_type=product_type,
                           max_stock=max_stock, relevant_fields=relevant_fields, variation_fields=variation_fields, random_products=random_())

@app.route('/get_price')
def get_price():
    product_id = request.args.get('product_id')
    product_type = request.args.get('product_type')
    diameter = request.args.get('diameter')
    meters = request.args.get('meters')

    if product_type not in product_models:
        return {'price': None}

    _, variation_model = product_models[product_type]
    variation = db.session.query(variation_model).filter_by(
        product_id=product_id, diameter=diameter, meters=meters
    ).first()

    if variation:
        return {'price': variation.price}
    else:
        return {'price': None}


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product_type = request.form.get('product_type')
    diameter = request.form.get('diameter')
    meters = request.form.get('meters')

    if product_type not in product_models:
        return redirect(url_for('cart'))  # Redirect to cart if product_type is invalid

    _, variation_model = product_models[product_type]
    variation = db.session.query(variation_model).filter_by(
        product_id=product_id, diameter=diameter, meters=meters
    ).first()

    if variation:
        # Store the cart item in the session
        if 'cart' not in session:
            session['cart'] = []

        cart_item = {
            'product_id': product_id,
            'product_type': product_type,
            'diameter': diameter,
            'meters': meters,
            'price': variation.price
        }

        session['cart'].append(cart_item)
        session.modified = True

    return redirect(url_for('cart'))




@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template("cart.html", cart_items=cart_items)

class MyForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enter')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = MyForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()

        if existing_user:
            flash("Username or email already in use. Please choose a different one.", 'danger')
            return redirect(url_for("signup"))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash("You have successfully signed up!", 'success')
        return redirect(url_for("index"))

    return render_template("signup.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.username == "admin" and user.password == "admin":
            return redirect(url_for('dashboard'))
        else:
            if user and user.password == form.password.data:
                session['user_id'] = user.id
                flash("You have successfully logged in!", 'success')
                return redirect(url_for("index"))
            else:
                flash("Invalid email or password. Please try again.", 'danger')

    return render_template("login.html", form=form)
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    id = IntegerField('Id', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    img_url = StringField('Image', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('fillespanje', 'Fillespanje'),
        ('flourocarbon', 'Flourocarbon'),
        ('shockleader', 'Shock Leader'),
        ('allround', 'All Round'),
        ('surfcasting', 'Surfcasting'),
        ('spinning', 'Spinning'),
        ('bolognese', 'Bolognese'),
        ('jigg', 'Jigg'),
        ('bolentino', 'Bolentino'),
        ('makineta', 'Makineta')
    ], validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

@app.route('/dashboard')
def dashboard():
    # if not session.get('user_id'):
    #     return redirect(url_for('login'))
    # user = User.query.get(session['user_id'])
    # if not user or not user.is_admin:
    #     return redirect(url_for('index'))
    return render_template("dashboard.html")


@app.route('/dashboard/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        category = form.category.data
        name = form.name.data
        id = form.id.data
        price = form.price.data
        stock = form.stock.data
        img = form.img_url.data
        description = form.description.data
        print(f"Category: {category}")
        print(f"Name: {name}")
        print(f"Price: {price}")
        print(f"Stock: {stock}")
        print(f"Description: {description}")
        print(f"Variations: {variations_data}")
        print(name)
        variations_data = request.form.getlist('variations')  # Get all variations data from form
        print(variations_data)
        product = Makineta(
            product_id=id,
            product_name=name,
            img_url=img,  # Replace with actual URL or logic
            description=description
        )
        db.session.add(product)
        db.session.commit()
        # Handle multiple variations
        for variation_data in variations_data:
            variation = ProductVariationMakineta(
                product_id=id,
                price=variation_data.get('price'),
                stock=variation_data.get('stock'),
                size=variation_data.get('size')
            )
            db.session.add(variation)
        db.session.commit()

        # Handle other categories similarly

        return redirect(url_for('dashboard'))

    return render_template('add_products.html', form=form)

@app.route('/dashboard/edit_product/<string:product_type>/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_type, product_id):
    # if not session.get('user_id'):
    #     return redirect(url_for('login'))
    # user = User.query.get(session['user_id'])
    # if not user or not user.is_admin:
    #     return redirect(url_for('index'))

    product_model, variation_model = product_models[product_type]
    product = db.session.query(product_model).filter_by(id=product_id).first_or_404()
    variation = db.session.query(variation_model).filter_by(product_id=product.id).first_or_404()

    form = ProductForm(
        product_name=product.product_name,
        img_url=product.img_url,
        category=product_type,
        diameter=variation.diameter,
        meters=variation.meters,
        price=variation.price,
        stock=variation.stock
    )

    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.img_url = form.img_url.data
        variation.diameter = form.diameter.data
        variation.meters = form.meters.data
        variation.price = form.price.data
        variation.stock = form.stock.data

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_product.html', form=form, product_type=product_type, product_id=product_id)


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)

