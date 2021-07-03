# forms for user
from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField,
                    PasswordField,)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email,Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class Creaet_Users_Form(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    # email = StringField('Email:')
    email = EmailField('Email',validators=[DataRequired()])

    phone = StringField('Phone')
    # phone = PhoneNumberField('Phone:',country_code='US', display_format='national')

    submit = SubmitField('Submit')
