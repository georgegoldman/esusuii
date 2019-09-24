from flask import Blueprint, render_template
from application.web_forms import RegistrationForm, LoginForm, AdminForm
from flask_login import login_required, current_user

view = Blueprint('view', __name__)


@view.route('/')
@view.route('/home')
def home():
    return render_template('home.html', title='eltd-home')


@view.route('/signup')
def signup():

    form = RegistrationForm()

    return render_template('signup.html', form=form, title='eltd-signup')


@view.route('/login')
def login():
    form = LoginForm()

    return render_template('login.html', form=form, title='eltd-login')

@view.route('/account_home')
@login_required
def account_home():


    return render_template('account_home.html', username=current_user.email)

@view.route('/admin_signup')
@login_required
def admin_signup():

    form = AdminForm()
    return render_template('admin-signup.html', form=form,)
