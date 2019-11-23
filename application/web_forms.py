from flask import Markup
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
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

class UpdateAccountInfoForm(FlaskForm):
    username = TextField('text', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    picture = FileField('Edit your profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already taken')

class ChangePasswordForm():
    password = PasswordField('password',  validators=[DataRequired(message='password required')])
    confirm_pwd = PasswordField('confirm password',  validators=[DataRequired(message='confirm password required'), EqualTo('password', message='Passwords must match')])
