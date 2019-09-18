from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app  = Flask(__name__)

app.config['DEBUG']=1
app.config['SECRET_KEY']='32RERFWEG2'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'

db = SQLAlchemy(app)

from application import models
db.create_all()

login_manager = LoginManager(app)

from application.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_message = u"sign in to access this paged"
login_manager.login_view = 'view.login'


from application.views import view
app.register_blueprint(view)

from application.auths import auth
app.register_blueprint(auth)
