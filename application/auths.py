from flask import Blueprint, render_template, redirect, url_for, flash
from application.web_forms import RegistrationForm, LoginForm
from application.models import User
from application import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            flash('user already exist!')
            return render_template('signup.html', form=form)

        user(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('view.login'))


@auth.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user.email==email and user.password==password:
            login_user(user)
            return redirect(url_for('view.account_home'))

        else:
            flash('wrong logs')
            return redirect(url_for('view.login'))

@auth.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('view.home'))
