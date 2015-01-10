from flask import render_template, redirect, url_for, flash, request, current_app
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.principal import identity_changed, Identity

from auth import app, db

from auth.utils import send_email, flash_errors

from auth.core import core
from auth.core.forms import LoginForm, RegistrationForm, ForgotPasswordForm, NewPasswordForm
from auth.core.models.user import User

@core.route("/")
@login_required
def home():
    return render_template("core/home.html")

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
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            return redirect(request.args.get("next") or url_for("core.home"))
        else:
            flash("Your password was incorrect!", "danger")
    else:
        flash_errors(form)
    return render_template("core/login.html", form=form)

@core.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.home"))

@core.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Some extra validation - we should check to see if there's already a user registered with either that email
        # or that username
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash("That username is already in use!", "danger")
            return redirect(url_for("core.register"))

        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash("That email address is already in use!", "danger")
            return redirect(url_for("core.register"))

        # Create user model
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        if app.config['FORCE_EMAIL_ACTIVATION']:
            # Set activation key
            new_user.generate_activation_key()

            # Printing the validation URL, for debug times
            print(url_for('core.validate_registration', username=new_user.username, key=new_user.activation_key))

            # Send the new user their activation code
            send_email(
                [new_user.email],
                "[WHAuth] Welcome to WHAuth, Please Activate Your Account",
                render_template(
                    'core/email_registration.txt',
                    username=new_user.username,
                    siteurl=url_for("core.home", _external=True),
                    activationurl=url_for("core.validate_registration", username=new_user.username, key=new_user.activation_key, _external=True)
                ),
                render_template(
                    'core/email_registration.html',
                    username=new_user.username,
                    siteurl=url_for("core.home", _external=True),
                    activationurl=url_for("core.validate_registration", username=new_user.username, key=new_user.activation_key, _external=True)
                )
            )

            post = url_for('core.post_register')
        else:
            new_user.activate()
            flash('Account created, you may now log in', 'success')
            post = url_for('core.home')

        # Save user
        db.session.add(new_user)
        db.session.commit()

        return redirect(post)
    else:
        flash_errors(form)
    return render_template("core/register.html", form=form)

@core.route("/register/validating")
def post_register():
    return render_template("core/post_register.html")

@core.route("/register/validate/<username>/<key>")
def validate_registration(username, key):
    user = User.query.filter_by(username=username, activation_key=key, active=False).first_or_404()
    user.activate()

    db.session.add(user)
    db.session.commit()

    flash("User '%s' has now been activated and you may log in." % (username,), "success")

    return redirect(url_for('core.login'))

@core.route("/login/forgot_password", methods=["GET", "POST"])
def forgotten_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.email.data).first()
        if not user:
            flash("Account not found!", "danger")
            return redirect(url_for('core.forgotten_password'))
        user.generate_activation_key()

        send_email(
            [user.email],
            "[WHAuth] Password Reset Link",
            render_template(
                'core/email_registration.txt',
                username=user.username,
                siteurl=url_for("core.home", _external=True),
                activationurl=url_for("core.reset_password", username=user.username, key=user.activation_key, _external=True)
            ),
            render_template(
                'core/email_registration.html',
                username=user.username,
                siteurl=url_for("core.home", _external=True),
                activationurl=url_for("core.reset_password", username=user.username, key=user.activation_key, _external=True)
            )
        )

        db.session.add(user)
        db.session.commit()

        flash("An email has been dispatched and you will have a password reset link shortly", "success")
        return redirect(url_for("core.login"))
    else:
        flash_errors(form)
    return render_template('core/forgot_password.html', form=form)

@core.route("/login/reset/<username>/<key>", methods=['GET', 'POST'])
def reset_password(username, key):
    user = User.query.filter_by(username=username, activation_key=key, active=True).first_or_404()
    form = NewPasswordForm()
    if form.validate_on_submit():
        user.activate()

        user.set_password(form.password.data)

        flash('Password changed successfully!', 'success')
        return redirect(url_for('core.home'))
    else:
        flash_errors(form)
    return render_template('core/reset_password.html', form=form)

@core.route("/profile")
@login_required
def profile():
    return render_template('core/profile.html')

@core.route("/profile/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = NewPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)

        flash('Password changed successfully!', 'success')
        return redirect(url_for('core.profile'))
    else:
        flash_errors(form)
    return render_template('core/change_password.html', form=form)