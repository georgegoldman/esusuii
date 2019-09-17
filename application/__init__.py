from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app  = Flask(__name__)

app.config['DEBUG']=1
app.config['SECRET_KEY']='32RERFWEG2'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'

db = SQLAlchemy(app)

from application import models
db.create_all()

from application.views import view
app.register_blueprint(view)

from application.auths import auth
app.register_blueprint(auth)
