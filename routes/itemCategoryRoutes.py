from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import databases.models as models
from databases.models.user import AccessRoleEnum
from databases.base import db
from forms import createItemCategoryForm

#Blueprints to define all routes linking to item category CRUD functions
itemCategory_bp = Blueprint('itemCategory', __name__)

@itemCategory_bp.route("/categories")
@login_required
def listCategories():
    itemCategories = models.ItemCategory.query.filter_by(isDeleted=False)
    deletedCategories = models.ItemCategory.query.filter_by(isDeleted=True).all()
    return render_template('itemCategory.html', itemCategories=itemCategories, deletedCategories=deletedCategories, AccessRoleEnum=AccessRoleEnum)

@itemCategory_bp.route("/categories/create", methods=['GET', 'POST'])
@login_required
def addItemCategory():
    form = createItemCategoryForm()
    if form.validate_on_submit():
        try:
            formInput = models.ItemCategory(itemCategoryName=form.itemCategoryName.data)
            db.session.add(formInput)
            db.session.commit()
            flash(f"Item category created successfully!", "success")
        except: 
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
    return render_template("addItemCategory.html", form=form)

@itemCategory_bp.route("/categories/update/<int:itemCategoryID>", methods=['GET', 'POST'])
@login_required
def updateCategory(itemCategoryID):
    category= db.session.get(models.ItemCategory, itemCategoryID)
    if category.isDeleted:
        flash(f"Item category is deleted", "warning")
        return redirect(url_for('itemCategory.listCategories'))
    form = createItemCategoryForm(obj=category)
    if form.validate_on_submit():
        try:
            category.itemCategoryName = form.itemCategoryName.data
            db.session.commit()
            flash(f"Item category updated successfully!", "success")
        except:
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
    return render_template("addItemCategory.html", form=form)

@itemCategory_bp.route("/categories/delete/<int:itemCategoryID>", methods=['GET', 'POST'])
@login_required
def deleteCategory(itemCategoryID):

    #forbid User roles from deleting
    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! You do not have permission to delete item categories", "danger")
        return redirect(url_for('itemCategory.listCategories'))

    category= db.session.get(models.ItemCategory, itemCategoryID)
    if category.isDeleted:
        flash(f"Item category already deleted", "warning")
        return redirect(url_for('itemCategory.listCategories'))
    category.isDeleted = True
    db.session.commit()
    flash(f"Item category deleted successfully!", "success")
    return redirect(url_for('itemCategory.listCategories'))

@itemCategory_bp.route("/categories/restore/<int:itemCategoryID>", methods=['GET'])
@login_required
def restoreCategory(itemCategoryID):
   #forbid User roles from restoring
    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! You do not have permission to restore item categories", "danger")
        return redirect(url_for('itemCategory.listCategories'))
    category= db.session.get(models.ItemCategory, itemCategoryID)
    if category.isDeleted:
        category.isDeleted = False
        db.session.commit()
        flash(f"Item category restored successfully!", "success")
    return redirect(url_for('itemCategory.listCategories'))