from flask import render_template, redirect, url_for
from flask.ext.login import login_required

from auth.core import core
from auth.core.forms import LoginForm, RegistrationForm

@core.route("/")
@login_required
def home():
    return render_template("core_home.html")

@core.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("core_login.html", form=form)

@core.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('core.post_register'))
    return render_template("core_register.html", form=form)

@core.route("/register/validating")
def post_register():
    return render_template("core_post_register.html")