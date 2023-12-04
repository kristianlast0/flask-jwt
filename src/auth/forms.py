from wtforms import StringField, PasswordField, validators
from flask_wtf import FlaskForm

class CredentialsForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired(), validators.Length(min=4, max=25), validators.Regexp('^[a-zA-Z0-9_]*$', message='Username must contain only letters, numbers or underscore')])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=8, max=25)])