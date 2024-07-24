from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap4

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_BINDS = {
        'fillespanje': 'sqlite:///fillespanje.db',
        'flourocarbon': 'sqlite:///flourocarbon.db'
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

# Define a model for the 'fillespanje' database
class Fillespanje(db.Model):
    __bind_key__ = 'fillespanje'
    __tablename__ = 'fillespanje'
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

class Flourocarbon(db.Model):
    __bind_key__ = 'flourocarbon'
    __tablename__ = 'flourocarbon'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

class ProductVariationFlourocarbon(db.Model):
    __bind_key__ = 'flourocarbon'
    __tablename__ = 'product_variation'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('flourocarbon.id'), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    meters = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    # Example usage
    new = Flourocarbon(id=1, product_name="Tubertini Bos", img_url="https://www.tubertini.it/media/__sized__/images/24760-24767-Fluorocarbon-Bos-thumbnail-533x400-70.jpg")
    new_2 = ProductVariationFlourocarbon(product_id=1, diameter=0.26, meters=50, price=1000)

    db.session.add(new)
    db.session.add(new_2)
    db.session.commit()
    return render_template("index.html")

@app.route('/fillespanje')
def fillespanje():
    products = db.session.query(Fillespanje).all()
    for product in products:
        product.variations = db.session.query(ProductVariation).filter_by(product_id=product.id).all()
    return render_template("fillespanje.html", products=products)

@app.route("/flourocarbon")
def flourocarbon():
    products = db.session.query(Flourocarbon).all()
    print(products)
    for product in products:
        product.variations = db.session.query(ProductVariationFlourocarbon).filter_by(product_id=product.id).all()
    return render_template("flourocarbon.html", products=products)


@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = db.session.query(Fillespanje).filter_by(id=product_id).first_or_404()
    variations = db.session.query(ProductVariation).filter_by(product_id=product.id).all()

    # Group variations by diameter and meters for easier handling in the template
    diameter_variations = {}
    meter_variations = {}

    for variation in variations:
        if variation.diameter not in diameter_variations:
            diameter_variations[variation.diameter] = []
        diameter_variations[variation.diameter].append(variation)

        if variation.meters not in meter_variations:
            meter_variations[variation.meters] = []
        meter_variations[variation.meters].append(variation)

    return render_template("product_details.html", product=product, diameter_variations=diameter_variations,
                           meter_variations=meter_variations)

@app.route('/get_price')
def get_price():
    product_id = request.args.get('product_id')
    diameter = request.args.get('diameter')
    meters = request.args.get('meters')

    variation = db.session.query(ProductVariation).filter_by(
        product_id=product_id, diameter=diameter, meters=meters
    ).first()

    if variation:
        return {'price': variation.price}
    else:
        return {'price': None}

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    diameter = request.form.get('diameter')
    meters = request.form.get('meters')

    # Retrieve the selected variation
    variation = db.session.query(ProductVariation).filter_by(
        product_id=product_id, diameter=diameter, meters=meters
    ).first()

    # Store the cart item in the session
    if 'cart' not in session:
        session['cart'] = []

    cart_item = {
        'product_id': product_id,
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


@app.route("/admin-dashboard")
def dashboard():

    return render_template("dashboard.html")



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
