from flask import abort
from application import admin
from flask_admin.contrib.sqla import ModelView
from . import db
from flask_login import current_user
from .models import User


class Fulcrum(ModelView):

    def is_accessible(self):
        if current_user.admin == True:
            return current_user.is_authenticated
        else:
            abort(404)
    def not_auth(self):
        if is_anonymous:
            return "you are not authorized to view this page"


admin.add_view(Fulcrum(User, db.session))
