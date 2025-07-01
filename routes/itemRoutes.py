from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import databases.models as models
from databases.models.user import AccessRoleEnum
from databases.base import db
from forms import createItemForm

#Blueprints to define all routes linking to item CRUD functions
item_bp = Blueprint('item', __name__)

@item_bp.route("/items")
@login_required
def listItems():
    items =  (
        db.session.query(
            models.Item.itemID,
            models.Vendor.vendorName,
            models.User.username, 
            models.ItemCategory.itemCategoryName, 
            models.Item.expiryDate, 
            models.Item.status, 
            models.Item.userNotes
            )
            .join(models.Vendor, models.Item.vendorID == models.Vendor.vendorID)
            .join(models.User, models.Item.userID == models.User.userID)
            .join(models.ItemCategory, models.Item.itemCategoryID == models.ItemCategory.itemCategoryID)
            .filter_by(isDeleted=False)
    )

    deletedItems =  (
        db.session.query(
            models.Item.itemID,
            models.Vendor.vendorName,
            models.User.username, 
            models.ItemCategory.itemCategoryName, 
            models.Item.expiryDate, 
            models.Item.status, 
            models.Item.userNotes
        )
            .join(models.Vendor, models.Item.vendorID == models.Vendor.vendorID)
            .join(models.User, models.Item.userID == models.User.userID)
            .join(models.ItemCategory, models.Item.itemCategoryID == models.ItemCategory.itemCategoryID)
            .filter(models.Item.isDeleted == True).all()
    )
    
    return render_template('item.html', items=items, deletedItems=deletedItems, AccessRoleEnum=AccessRoleEnum)

@item_bp.route("/items/create", methods=['GET', 'POST'])
@login_required
def addItem():
    form = createItemForm()
    if form.validate_on_submit():
        try:
            print(f"vendorID: {form.vendorID.data}")
            formInput = models.Item(vendorID=form.vendorID.data.vendorID, userID=form.userID.data.userID, itemCategoryID=form.itemCategoryID.data.itemCategoryID, expiryDate=form.expiryDate.data, status=form.status.data, userNotes=form.userNotes.data )
            db.session.add(formInput)
            db.session.commit()
            flash(f"Item created successfully!", "success")
        except: 
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
    return render_template("addItem.html", form=form)

@item_bp.route("/items/update/<int:itemID>", methods=['GET', 'POST'])
@login_required
def updateItem(itemID):
     item= db.session.get(models.Item, itemID)
     if item.isDeleted:
         flash(f"Item is deleted", "warning")
         return redirect(url_for('item.listItems'))
     form = createItemForm(obj=item)
     if form.validate_on_submit():
        try:
            item.vendorID=form.vendorID.data.vendorID
            item.userID=form.userID.data.userID
            item.itemCategoryID=form.itemCategoryID.data.itemCategoryID
            item.expiryDate=form.expiryDate.data
            item.status=form.status.data
            item.userNotes=form.userNotes.data
            db.session.commit()
            flash(f"Item updated successfully!", "success")
        except:
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
     return render_template("addItem.html", form=form)

@item_bp.route("/items/delete/<int:itemID>", methods=['GET', 'POST'])
@login_required
def deleteItem(itemID):

    #forbid User roles from deleting
    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! You do not have permission to delete items", "danger")
        return redirect(url_for('item.listItems'))

    item= db.session.get(models.Item, itemID)
    if item.isDeleted:
        flash(f"Item already deleted", "warning")
        return redirect(url_for('item.listItems'))
    item.isDeleted = True
    db.session.commit()
    flash(f"Item deleted successfully!", "success")
    return redirect(url_for('item.listItems'))

@item_bp.route("/items/restore/<int:itemID>", methods=['GET'])
@login_required
def restoreItem(itemID):
   #forbid User roles from restoring
    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! You do not have permission to restore items", "danger")
        return redirect(url_for('item.listItems'))
    item= db.session.get(models.Item, itemID)
    if item.isDeleted:
        item.isDeleted = False
        db.session.commit()
        flash(f"Item restored successfully!", "success")
    return redirect(url_for('item.listItems'))
