from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length 

class createVendorForm(FlaskForm):
    vendorName = StringField('Vendor Name', validators = [DataRequired(), length(max=50)], render_kw={"placeholder": "Enter vendor name", "class": "form-control"}) 
    sustainabilityCertified = BooleanField('Sustainability Certified')
    submit = SubmitField('Add new vendor')