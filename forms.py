from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField, TimeField, IntegerField
from wtforms.validators import InputRequired, NumberRange, number_range

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message='Cannot be empty.')])
    note = TextAreaField('Note', validators=[InputRequired(message='Cannot be empty.')])
    submit = SubmitField('Submit')
    update = SubmitField('Update')
    start_time = StringField('Start Time', validators=[InputRequired(message='Must be set.')])
    duration = IntegerField('Task Duration (min)', validators=[NumberRange(min=1, max=59, message='number between 1-59')])

