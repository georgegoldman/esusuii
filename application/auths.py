import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, request, Markup
from application.web_forms import RegistrationForm, LoginForm, AdminForm, GroupForm, UpdateAccountInfoForm
from application.models import User, Group, Member
from application import db, app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():

    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        username = form.username.data

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Log details aready taken')
            return render_template('signup.html', form=form)


        user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        flash('your acount have been created.\nThank you for dealing with Esusu')
        return redirect(url_for('view.login'))

    flash('check your email or passwords if they\'re correct !')
    return redirect(url_for('view.signup'))

@auth.route('/login', methods=['POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('view.account_home'))

        else:
            flash(Markup("Check your login details or account does not exit ! please <a href='/signup' class='alert-link'>signup</a>"))
            return redirect(url_for('view.login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@auth.route('/upd_acct_info', methods=['GET','POST'])
@login_required
def upd_acct_info():

    form = UpdateAccountInfoForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profil_pix = picture_file
        current_user.username =  form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('account details updated')
        return redirect(url_for('view.account_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pix = url_for('static', filename=f'images/{current_user.profil_pix}')
    return render_template('account_home.html', form=form, current_user=current_user, profile_pix=profile_pix)

@auth.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('view.login'))
