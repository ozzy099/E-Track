from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
# from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from databases.createDatabase import hashPassword
import databases.models as models
from databases.base import db
from forms import registerForm, loginForm


#Blueprints to define all routes linking to user authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    error = ""
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if models.User.query.filter_by(username=username).first():
           return render_template("register.html", error = "username address already taken", form=form)

        # hashedPassword = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        hashedPassword = hashPassword(password)

        formInput = models.User(firstName=form.firstName.data, lastName=form.lastName.data, username=username, password=hashedPassword, accessRole=form.accessRole.data)
        try:
            db.session.add(formInput)
            db.session.commit()
            flash(f"User registered successfully!", "success") 
        except Exception as e:
            db.session.rollback()
            flash(f"Something went wrong. Please try again.", "danger")
            error="An issue occured whilst registering. Please contact an Admin for queries"
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form, error=error)


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = models.User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            login_user(user)
            return redirect(url_for("main.home"))
        else:
            return render_template("login.html", error="Invalid username or password", form=form)
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))