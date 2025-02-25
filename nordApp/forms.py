from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password")
    role = StringField('Role', validators = [DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    name = StringField('Name',validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

