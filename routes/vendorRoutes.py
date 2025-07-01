from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
import databases.models as models
from databases.models.user import AccessRoleEnum
from databases.base import db
from forms import createVendorForm

#Blueprints to define all routes linking to vendor CRUD functions
vendor_bp = Blueprint('vendor', __name__)

@vendor_bp.route("/vendors")
@login_required
def listVendors():
    vendors = models.Vendor.query.filter_by(isDeleted=False)
    deletedVendors = models.Vendor.query.filter_by(isDeleted=True).all()
    return render_template('vendor.html', vendors=vendors, deletedVendors=deletedVendors, AccessRoleEnum=AccessRoleEnum)

@vendor_bp.route("/vendors/create", methods=['GET', 'POST'])
@login_required
def addVendor():
    form = createVendorForm()
    if form.validate_on_submit():
        try:
            formInput = models.Vendor(
                vendorName=form.vendorName.data,
                sustainabilityCertified=form.sustainabilityCertified.data
            )
            db.session.add(formInput)
            db.session.commit()
            flash(f"Vendor added successfully!", "success")
        except:
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
    return render_template("addVendor.html", form=form)

@vendor_bp.route("/vendors/update/<int:vendorID>", methods=['GET', 'POST'])
@login_required
def updateVendor(vendorID):
    vendor = db.session.get(models.Vendor, vendorID)
    if vendor.isDeleted:
         flash(f"Vendor is deleted", "warning")
         return redirect(url_for('vendor.listVendors'))
    form = createVendorForm(obj=vendor)
    if form.validate_on_submit():
        try:
            vendor.vendorName = form.vendorName.data
            vendor.sustainabilityCertified = form.sustainabilityCertified.data
            db.session.commit()
            flash(f"Vendor updated successfully!", "success")
        except:
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
    return render_template("addVendor.html", form=form)

@vendor_bp.route("/vendors/delete/<int:vendorID>", methods=['GET', 'POST'])
@login_required
def deleteVendor(vendorID):
    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! Access denied! You do not have permission to delete vendors", "danger")
        return redirect(url_for('vendor.listVendors'))
    vendor = db.session.get(models.Vendor, vendorID)
    if vendor.isDeleted:
         flash(f"Vendor already deleted", "warning")
         return redirect(url_for('vendor.listVendors'))
    vendor.isDeleted = True
    db.session.commit()
    flash(f"Vendor deleted successfully!", "success")
    return redirect(url_for('vendor.listVendors'))

@vendor_bp.route("/vendors/restore/<int:vendorID>", methods=['GET', 'POST'])
@login_required
def restoreVendor(vendorID):
    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! Access denied! You do not have permission to restore vendors", "danger")
        return redirect(url_for('vendor.listVendors'))
    vendor = db.session.get(models.Vendor, vendorID)
    if vendor.isDeleted:
        vendor.isDeleted = False
        db.session.commit()
        flash(f"Vendor restored successfully!", "success")
    return redirect(url_for('vendor.listVendors'))