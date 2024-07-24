from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

class Config:
    # Database URI for the 'users' database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'

    # Additional bindings for the 'fillespanje' database
    SQLALCHEMY_BINDS = {
        'produktet': 'sqlite:///produketet.db'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, session_options={"autoflush": False, "expire_on_commit": False})

# Define a model for the 'users' database
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

# Define a model for the 'fillespanje' database
class Fillespanje(db.Model):
    __bind_key__ = 'produktet'
    __tablename__ = 'produktet'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(250), nullable=False)
    types = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

@app.route('/')
def index():
    # # Example usage: Adding entries to both databases
    # user = User(username='testuser', email='test@example.com', password="test")
    # fillespanje_item = Fillespanje(product_name='test', price=59.99,type="test" , types="0.22",  img_url="test")
    #
    # db.session.add(user)
    # db.session.add(fillespanje_item)
    # db.session.commit()
    # db.session.close()

    return render_template("index.html")

@app.route('/fillespanje')
def fillespanje():
    products = db.session.execute(db.select(Fillespanje).where(Fillespanje.type == "fillespanje")).scalars()
    for i in products:
        print(i.price)
    return "Hello"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables for both databases
    app.run(debug=True)
