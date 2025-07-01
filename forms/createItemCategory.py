from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length 

class createItemCategoryForm(FlaskForm):
    itemCategoryName = StringField('Item Category', validators=[DataRequired(), length(max=120)], render_kw={"placeholder": "Enter item category", "class": "form-control"})
    submit = SubmitField('Add new Item Category')