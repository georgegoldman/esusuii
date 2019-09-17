from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from application.models import User

class RegistrationForm(FlaskForm):
    ''' registration form '''

    username = TextField('username', validators=[InputRequired(message='username required'), Length(min=4, max=25, message='Username must be up to 4 and 25 character')])

    email = TextField('email',  validators=[InputRequired(message='email required'), Length(min=4, max=100, message='Email must be up to 4 and 25 character')])

    password = PasswordField('password',  validators=[InputRequired(message='password required'), Length(min=4, max=25, message='Password must be up to 4 and 25 character')])

    confirm_pwd = PasswordField('confirm password',  validators=[InputRequired(message='confirm password required'), EqualTo('password', message='Passwords must match')])

    submit_button = SubmitField('Create')

    def validate_email(self, email):
        email_object = User.query.filter_by(email=email.data).first()
        if email_object:
            raise ValidationError("email already exit. Select a different email.")
