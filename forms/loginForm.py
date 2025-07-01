from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField
from wtforms.validators import InputRequired, length



class loginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('username required'), length(min=5, max=50, message='Username must be in 5 to 50 characters')])
    password = PasswordField('Password',validators=[InputRequired('Password required'), length(min=8)])
    submit = SubmitField('Submit')