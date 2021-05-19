import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login.config import LOGIN_MESSAGE
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


login_manager = LoginManager()
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Often people will also separate these into a separate config.py file 
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager.init_app(app)
db = SQLAlchemy(app)
Migrate(app,db)

from lib_project.users.views import users_blueprints
from lib_project.books.views import books_blueprints
# from lib_project.users.views import users_blueprints

app.register_blueprint(users_blueprints, url_prefix='/users')
app.register_blueprint(books_blueprints, url_prefix='/books')
# login_manager.login_view = 'login'
# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
# 當使用者還沒登入，卻請求了一個需要登入權限才能觀看的網頁時，我們就先送使用找到login_view所指定的位置來
login_manager.login_view = "users.login"
