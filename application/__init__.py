from flask import Flask, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_fontawesome import FontAwesome

app = Flask(__name__)

app.config['DEBUG']=1
app.config['SECRET_KEY']='32RERFWEG2'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/esusu'




db = SQLAlchemy(app)
migrate =  Migrate(app, db)
fa = FontAwesome(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


from application import models
db.create_all()

login_manager = LoginManager(app)

from application.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.login_view = 'auth.login'
login_manager.login_message = Markup("hello please can you login or <a href='/signup' class='alert-link'>signup</a> up thanks")


from application.views import view
app.register_blueprint(view)

from application.auths import auth
app.register_blueprint(auth)

from application.oplogic import oplogic
app.register_blueprint(oplogic)
