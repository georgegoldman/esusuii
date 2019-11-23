import os
from flask import Flask, Markup
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_fontawesome import FontAwesome
from flask_mail import Mail

app = Flask(__name__)

app.config['DEBUG']=True
app.config['SECRET_KEY']= 'duhwuheu234532i0290k@{{@~@nirjgir}}'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:password@localhost/esusu'
app.config.update(
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = '587',
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'georgegoldman2014@gmail.com',
    MAIL_PASSWORD = 'Goldman14'
)




db = SQLAlchemy(app)
fa = FontAwesome(app)
mail = Mail(app)
scheduler = APScheduler(app)


from application import models
db.create_all()

login_manager = LoginManager(app)

from application.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.login_view = 'auth.login'
login_manager.login_message = Markup("hello, please login or <a href='/signup' class='alert-link'>signup</a> up thanks")


from application.views import view
app.register_blueprint(view)

from application.auths import auth
app.register_blueprint(auth)

from application.oplogic import oplogic
app.register_blueprint(oplogic)
