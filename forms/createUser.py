from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, length
from databases.models.user import AccessRoleEnum


class createUserForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), length(min=2, max=50)], render_kw={"placeholder": "Enter first name", "class": "form-control"})
    lastName = StringField('Last Name', validators=[DataRequired(), length(min=2, max=50)], render_kw={"placeholder": "Enter last name", "class": "form-control"})
    username = StringField('Username', validators=[DataRequired(), length(min=5, max=25)], render_kw={"placeholder": "Enter username", "class": "form-control"})
    password = StringField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter password", "class": "form-control"})
    accessRole = SelectField('Access Role', choices=[(category.name) for category in AccessRoleEnum], validators=[DataRequired()], render_kw={"placeholder": "Select Access Level", "class": "form-control"})
    submit = SubmitField('Add new User')