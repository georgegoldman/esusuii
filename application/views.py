from flask import Blueprint, render_template
from application.web_forms import RegistrationForm

view = Blueprint('view', __name__)


@view.route('/')
@view.route('/home')
def home():
    return render_template('home.html', title='eltd-home')
@view.route('/signup')
def signup():

    reg_form = RegistrationForm()

    return render_template('signup.html', form=reg_form, title='eltd-signup')
