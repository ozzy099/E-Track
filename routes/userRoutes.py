from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import databases.models as models
from databases.models.user import AccessRoleEnum    
from databases.base import db
from forms import createUserForm
# from werkzeug.security import generate_password_hash
from databases.createDatabase import hashPassword
import bcrypt

#Blueprints to define all routes linking to user CRUD functions
user_bp = Blueprint('user', __name__)

@user_bp.route("/users")
@login_required
def listUsers():
    users = models.User.query.filter_by(isDeleted=False)
    deletedUsers = models.User.query.filter_by(isDeleted=True).all()
    return render_template('user.html', users=users, deletedUsers=deletedUsers, AccessRoleEnum=AccessRoleEnum)

@user_bp.route("/users/create", methods=['GET', 'POST'])
@login_required
def addUser():
    form = createUserForm()
    if form.validate_on_submit():
        try:
            
            formInput = models.User(firstName=form.firstName.data, lastName=form.lastName.data, username=form.username.data, password=hashPassword(form.password.data), accessRole=form.accessRole.data)
            db.session.add(formInput)
            db.session.commit()
            flash(f"User added successfully!", "success") 
        except: 
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
    return render_template("addUser.html", form=form)

@user_bp.route("/users/update/<int:userID>", methods=['GET', 'POST'])
@login_required
def updateUser(userID):
    user= db.session.get(models.User, userID)
    if user.isDeleted:
         flash(f"User is deleted", "warning")
         return redirect(url_for('user.listUsers'))
    form = createUserForm(obj=user)
    if form.validate_on_submit():
        try:
            user.firstName = form.firstName.data
            user.lastName=form.lastName.data
            user.username=form.username.data
            enteredPassword = form.password.data
            hashedPassword = hashPassword(enteredPassword)
            user.password = hashedPassword
            user.accessRole=form.accessRole.data
            db.session.commit()
            flash(f"User updated successfully!", "success") 
        except:
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
    return render_template("addUser.html", form=form)

@user_bp.route("/users/delete/<int:userID>", methods=['GET', 'POST'])
@login_required
def deleteUser(userID):

    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! You do not have permission to delete users", "danger")
        return redirect(url_for('user.listUsers'))

    user= db.session.get(models.User, userID)
    if user.isDeleted:
         flash(f"User already deleted", "warning")
         return redirect(url_for('user.listUsers'))
    user.isDeleted = True
    db.session.commit()
    flash(f"User deleted successfully!", "success")
    return redirect(url_for('user.listUsers'))

@user_bp.route("/users/restore/<int:userID>", methods=['GET'])
@login_required
def restoreUser(userID):
    if current_user.accessRole == AccessRoleEnum.User:
        flash(f"Access denied! You do not have permission to restore users", "danger")
        return redirect(url_for('user.listUsers'))
    user= db.session.get(models.User, userID)
    if user.isDeleted:
        user.isDeleted = False
        db.session.commit()
        flash(f"User restored successfully!", "success")
    return redirect(url_for('user.listUsers'))
