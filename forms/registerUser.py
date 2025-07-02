from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, length
from databases.models.user import AccessRoleEnum

class registerForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), length(min=2,max=50)], render_kw={"placeholder": "Enter first name", "class": "form-control"})
    lastName = StringField('Last Name', validators=[DataRequired(), length(min=2, max=50)], render_kw={"placeholder": "Enter last name", "class": "form-control"})
    username = StringField('Username', validators=[DataRequired(), length(min=5, max=25)], render_kw={"placeholder": "Enter username", "class": "form-control"})
    password = StringField('Password', validators=[DataRequired(), length(min=8)], render_kw={"placeholder": "Enter password", "class": "form-control"})
    accessRole = HiddenField(default='User')
    submit = SubmitField('Register')