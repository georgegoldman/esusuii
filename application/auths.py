from flask import Blueprint, render_template, redirect, url_for
from application.web_forms import RegistrationForm
from application.models import User
from application import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return 'insert into db'

    return render_template('signup.html', form=reg_form)
