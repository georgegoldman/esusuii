from flask import Blueprint, render_template
from application.web_forms import RegistrationForm

view = Blueprint('view', __name__)

@view.route('/')
def hello():
    return render_template('hello.html')

@view.route('/home')
def home():
    return render_template('home.html', title='eltd-home')

@view.route('/signup', methods=['POST', 'GET'])
def signup():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return 'great success'

    return render_template('signup.html', form=reg_form, title='eltd-signup')
