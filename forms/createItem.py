from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, length
from wtforms_sqlalchemy.fields import QuerySelectField
from databases.models.item import StatusEnum
from databases.createDatabase import db
import databases.models as models

#function to get all existing UserIDs
def allUsers():
    users: list[models.User]= db.session.query(models.User).filter_by(isDeleted=False)
    for u in users:
        yield u

#function to get all existing vendorIDs
def allVendors():
    vendors: list[models.Vendor]= db.session.query(models.Vendor).filter_by(isDeleted=False)
    for v in vendors:
        yield v

#function to get all existing itemCategoryIDs
def allItemCategories():
    itemCategories: list[models.ItemCategory]= db.session.query(models.ItemCategory).filter_by(isDeleted=False)
    for i in itemCategories:
        yield i

class createItemForm(FlaskForm):
    vendorID= QuerySelectField("Vendor", query_factory=allVendors, validators=[DataRequired(), ])
    userID = QuerySelectField("User", query_factory=allUsers, validators=[DataRequired()])
    itemCategoryID = QuerySelectField("Item Category", query_factory=allItemCategories, validators=[DataRequired()])
    expiryDate = DateField("Expiry Date", validators=[DataRequired()])
    status = SelectField("Status", choices=[(category.name) for category in StatusEnum], validators=[DataRequired()])
    userNotes = StringField("Optional User Notes", validators=[length(max=100)], render_kw={"placeholder": "Enter optional notes", "class": "form-control"})
    submit = SubmitField('Add new Item')