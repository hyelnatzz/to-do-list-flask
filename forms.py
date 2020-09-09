from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message='Cannot be empty.')])
    note = TextAreaField('Note', validators=[InputRequired(message='Cannot be empty.')])
    submit = SubmitField('Submit')
    update = SubmitField('Update')

