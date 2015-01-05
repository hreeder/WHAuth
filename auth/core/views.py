from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, login_user, logout_user

from auth import db

from auth.utils import send_email, flash_errors

from auth.core import core
from auth.core.forms import LoginForm, RegistrationForm, ForgotPasswordForm
from auth.core.models.user import User

@core.route("/")
@login_required
def home():
    return render_template("core_home.html")

@core.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data,
            active=True
        ).first()
        if not user:
            flash("User account not found!", "danger")
            return redirect(url_for("core.login"))

        if user.validate_password(form.password.data):
            login_user(user)
            return redirect(request.args.get("next") or url_for("core.home"))
        else:
            flash("Your password was incorrect!", "danger")
    else:
        flash_errors(form)
    return render_template("core_login.html", form=form)

@core.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.home"))

@core.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create user model
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        # Set activation key
        new_user.generate_activation_key()
        print(new_user.activation_key)
        print(url_for('core.validate_registration', username=new_user.username, key=new_user.activation_key))

        # Save user
        db.session.add(new_user)
        db.session.commit()

        # Send the new user their activation code
        # send_email()
        return redirect(url_for('core.post_register'))
    else:
        flash_errors(form)
    return render_template("core_register.html", form=form)

@core.route("/register/validating")
def post_register():
    return render_template("core_post_register.html")

@core.route("/register/validate/<username>/<key>")
def validate_registration(username, key):
    user = User.query.filter_by(username=username, activation_key=key, active=False).first_or_404()
    user.activate()

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('core.login'))

@core.route("/login/forgot_password")
def forgotten_password():
    form = ForgotPasswordForm()

    return render_template('core_forgot_password.html', form=form)