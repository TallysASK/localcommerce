from flask import Flask, render_template, request, url_for, session, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import os
from dotenv import load_dotenv
from db import db
from models import Loja
from Blueprints.auth import auth_bp
from Blueprints.store import store_bp

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# Config db

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + os.path.join(basedir, "instance/database.db")
    
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Config login manager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return db.session.get(Loja, int(id))

# Rotas

@app.route("/")
def home():
    lojas = Loja.query.all()
    return render_template("home.html", lojas=lojas)
    
# Blueprints

app.register_blueprint (auth_bp)
app.register_blueprint (store_bp)

# Inicializar
        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)