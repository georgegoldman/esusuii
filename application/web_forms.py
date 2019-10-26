from flask import Markup
from flask_wtf import FlaskForm
from flask_wtf.html5 import NumberInput
from wtforms import TextField, PasswordField, SubmitField, StringField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import  Length, EqualTo, ValidationError, DataRequired, Email
from application.models import User, Member



class RegistrationForm(FlaskForm):
    ''' registration form '''

    email = EmailField('email',  validators=[DataRequired(message='email required'), Email()])
    username = StringField('username', validators=[DataRequired(message='username required')])
    password = PasswordField('password',  validators=[DataRequired(message='password required')])
    confirm_pwd = PasswordField('confirm password',  validators=[DataRequired(message='confirm password required'), EqualTo('password', message='Passwords must match')])
    submit_button = SubmitField('Create')



class LoginForm(FlaskForm):

    '''login form'''

    email = EmailField('email',  validators=[DataRequired(message='email required'), Email()])
    password = PasswordField('password',  validators=[DataRequired()])
    submit_button = SubmitField(f'login')

class AdminForm(FlaskForm):

    '''admin signup'''
    email = EmailField('email',  validators=[DataRequired(message='email required'), Email()])
    password = PasswordField('password',  validators=[DataRequired(message='password required')])
    submit_button = SubmitField('Ugrade')

class GroupForm(FlaskForm):

    '''group signup'''

    group_name = StringField('group name', validators=[DataRequired(),])
    group_target = IntegerField(widget=NumberInput(), validators=[DataRequired()])
    member_limit = IntegerField(widget=NumberInput(), validators=[DataRequired()])
    submit_button = SubmitField('Create')


class ChangeAdminForm(FlaskForm):
    members_id = IntegerField(widget=NumberInput(), validators=[DataRequired()])
    change = SubmitField('Change')
