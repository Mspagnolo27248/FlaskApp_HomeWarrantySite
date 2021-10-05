import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_manager


login_manager = LoginManager()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#app congigurations
app.config['SECRET_KEY'] = 'Lorenzo93'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL2','sqlite:///'+os.path.join(basedir,'data.db'))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#SQLAlchemy Configuration
db = SQLAlchemy(app) #binds the classes in app to the sqlalchemy orm


Migrate(db,app)

login_manager.init_app(app)
login_manager.login_view = 'login' #This tell them to go to the /login view







