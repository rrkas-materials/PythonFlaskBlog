from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '1ee79fcbd2bb2730153928946a4ec1fb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# indicates that site.db is to be created in same directory as this file

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_func'
login_manager.login_message_category = 'info'

from . import routes
