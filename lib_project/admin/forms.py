# forms for admins

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class Add_User_form(FlaskForm):
    user_name = StringField('Name of Books:')
    submit = SubmitField('Add Book')
