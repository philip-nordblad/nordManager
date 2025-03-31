from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField, SubmitField, TimeField, FieldList, FormField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from datetime import datetime


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

class ShiftForm(FlaskForm):

    start_time = DateTimeField('Start Time',format ='%Y-%m-%d %H:%M',validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M', validators =[DataRequired()])
    submit = SubmitField('Create Shift')
    
class DayAvailabilityForm(FlaskForm):
    available = BooleanField("Available", default=False)
    all_day = BooleanField("All Day", default=False)
    start_time = TimeField("Start Time", validators=[Optional()])
    end_time = TimeField("End Time", validators=[Optional()])


# Define the main form
class AvailabilityForm(FlaskForm):
    total_hours = IntegerField("Desired Hours per Week", validators=[DataRequired(), lambda form, field: field.data > 0 or field.errors.append("Value must be positive")])
    days = FieldList(FormField(DayAvailabilityForm), min_entries=7)
    submit = SubmitField("Submit")

