from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import  Length, EqualTo, ValidationError, DataRequired, Email
from application.models import User



class RegistrationForm(FlaskForm):
    ''' registration form '''

    email = EmailField('email',  validators=[DataRequired(message='email required'), Email()])

    password = PasswordField('password',  validators=[DataRequired(message='password required')])

    confirm_pwd = PasswordField('confirm password',  validators=[DataRequired(message='confirm password required'), EqualTo('password', message='Passwords must match')])

    submit_button = SubmitField('Create')



class LoginForm(FlaskForm):

    '''login form'''

    email = EmailField('email',  validators=[DataRequired(message='email required'), Email()])

    password = PasswordField('password',  validators=[DataRequired()])

    submit_button = SubmitField('Log in')

class AdminForm(FlaskForm):

    '''admin signup'''
    email = EmailField('email',  validators=[DataRequired(message='email required'), Email()])

    password = PasswordField('password',  validators=[DataRequired(message='password required')])

    submit_button = SubmitField('Create')

class GroupForm(FlaskForm):

    '''group signup'''

    group_name = StringField('group name', validators=[DataRequired(),])

    group_target = IntegerField('group target', validators=[DataRequired()])

    submit_button = SubmitField('Create')
