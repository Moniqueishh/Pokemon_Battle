# This is how flask knows what to do with it's self. This explains flask is
from flask import Flask

from config import Config

from .auth.routes import auth
from .pokemon.routes import pokemon

from .models import db, User, Pokemon, teams
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(pokemon)

from . import routes 