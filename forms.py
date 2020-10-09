
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, TimeField, IntegerField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, number_range,EqualTo

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message='Cannot be empty.')])
    note = TextAreaField('Note', validators=[InputRequired(message='Cannot be empty.')])
    submit = SubmitField('Submit')
    update = SubmitField('Update')
    start_time = StringField('Start Time', validators=[InputRequired(message='Must be set.')])
    duration = IntegerField('Task Duration (min)', validators=[NumberRange(min=1, max=59, message='number between 1-59')])

class loginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='username is required')])
    password = PasswordField('password', validators=[InputRequired(message='password cannot be empty'), Length(min=8, message='password most be atleast 8 characters long')])
    remember = BooleanField('remember me?')
    login = SubmitField('Log In')


class signUpForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='username is required')])
    full_name = StringField('full name', validators=[InputRequired(message='full name required')])
    email = StringField('email', validators=[InputRequired(message='email is required')])
    password = PasswordField('password', validators=[InputRequired(message='password is required'),Length(min=8,message='password most be atleast 8 characters long')])
    confirm_password = PasswordField('confirm password', validators=[InputRequired(message='password is required'), EqualTo('password', message='password must match'), Length(min=8, message='password most be atleast 8 characters long')])
    signup = SubmitField('Sign Up')
    
    
    
