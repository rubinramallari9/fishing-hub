from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, FieldList, FormField, EmailField, SubmitField, Form, HiddenField, DecimalField
from wtforms.validators import DataRequired, Email, Optional
from functools import wraps
from random import sample
from sqlalchemy import func

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
app.config.from_object(Config)
app.secret_key = 'deal23-1B'  # Needed for session management

# Initialize CSRF protection


# Initialize SQLAlchemy
db = SQLAlchemy(app, session_options={"autoflush": False, "expire_on_commit": False})

# Define models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)

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
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Admin-only decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        user = User.query.filter_by(id=session['user_id']).first()
        if not user or not user.is_admin:
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

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
    categories = [
        'fillespanje', 'flourocarbon', 'shockleader', 'allround',
        'surfcasting', 'beach', 'spinning', 'bolognese', 'jigg',
        'bolentino', 'makineta'
    ]
    products = {}
    for category in categories:
        model = globals()[category.capitalize()]
        random_product = model.query.order_by(func.random()).first()
        if random_product:
            products[category] = random_product
    return render_template('index.html', products=products, random_products=random_())

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
    chosen_categories = sample(all_categories, min(4, len(all_categories)))

    random_products = {}

    for category in chosen_categories:
        product_model, _ = product_models[category]
        product = db.session.query(product_model).order_by(func.random()).first()
        if product:
            random_products[category] = product
    return random_products

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['email'] = user.email
            session['is_admin'] = user.is_admin
            return redirect(url_for('admin_dashboard' if user.is_admin else 'index'))
        flash("Invalid email or password", "error")
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

# Admin dashboard route
@app.route('/admin_dashboard')
# @admin_required
def admin_dashboard():
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

        for i in range(len(variation_diameters)):
            diameter = variation_diameters[i]
            price = variation_prices[i]
            stock = variation_stocks[i]

            variation = ProductVariationFlourocarbon(
                product_id=new_product.id,
                diameter=diameter,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_fillespanje.html')

@app.route('/dashboard/add_product/shockleader', methods=['GET', 'POST'])
def add_product_shockleader():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        img_url = request.form['img_url']
        description = request.form.get('description', '')

        # Create and add the main product
        new_product = ShockLeader(
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

        for i in range(len(variation_diameters)):
            diameter = variation_diameters[i]
            price = variation_prices[i]
            stock = variation_stocks[i]

            variation = ProductVariationShockLeader(
                product_id=new_product.id,
                diameter=diameter,
                price=float(price),
                stock=int(stock)
            )
            db.session.add(variation)

        db.session.commit()

        flash('Product and its variations added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_fillespanje.html')



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
    model = globals()[product_type.capitalize()]
    product = model.query.get_or_404(product_id)
    variation_model = globals()[f'ProductVariation{product_type.capitalize()}']
    variations = variation_model.query.filter_by(product_id=product_id).all()

    # Determine relevant fields based on product type
    if product_type in ['spinning', 'allround', 'surfcasting', 'bolognese', 'jigg', 'bolentino']:
        relevant_fields = ['meters', 'action']
    elif product_type == 'makineta':
        relevant_fields = ['size']
    elif product_type == 'fillespanje':
        relevant_fields = ['diameter', 'meters']
    else:
        relevant_fields = ['diameter']

    # Calculate the maximum stock value
    max_stock = max(variation.stock for variation in variations) if variations else 0

    return render_template('product_details.html', product=product, variations=variations, product_type=product_type, max_stock=max_stock, relevant_fields=relevant_fields, random_products=random_())



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
