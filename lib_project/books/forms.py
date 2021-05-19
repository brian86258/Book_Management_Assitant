# forms for user
from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField,
                    PasswordField,)


class Search_Book_Form(FlaskForm):
    search = StringField('Enter name of the book or ISBN:')
    submit = SubmitField("Submit")
