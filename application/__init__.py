from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app  = Flask(__name__)

app.config['DEBUG']=1
app.config['SECRET_KEY']='32RERFWEG2'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'

db = SQLAlchemy(app)

from application import models

from application.views import view
app.register_blueprint(view)

db.create_all()
