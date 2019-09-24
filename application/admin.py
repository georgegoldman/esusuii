from flask import abort
from application import admin
from flask_admin.contrib.sqla import ModelView
from . import db
from flask_login import current_user
from .models import User


class Fulcrum(ModelView):

    def is_accessible(self):
        try:
            if current_user.is_admin == True:
                return current_user.is_authenticated
            else:
                return abort(404)
        except AttributeError:
            return abort(404)

    #return current_user.is_authenticated
    def not_auth(self):
        return abort(404)


admin.add_view(Fulcrum(User, db.session))
