from flask import render_template, redirect, url_for
from flask.ext.login import login_required

from auth import db
from auth.admin import admin, admin_view_users, admin_toggle_account_status
from auth.utils import superuser_required
from auth.core.models.user import User

@admin.route("/users")
@login_required
@admin_view_users.require(403)
def list_users():
    all = User.query.all()

    return render_template(
        "admin/users/list.html",
        all_users=all
    )

@admin.route("/users/<username>")
@login_required
@admin_view_users.require(403)
def view_user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template(
        "admin/users/profile.html",
        user=user
    )

@admin.route("/users/<username>/toggle_superuser")
@login_required
@superuser_required
def toggle_superuser(username):
    user = User.query.filter_by(username=username).first_or_404()
    user.superuser = not user.superuser
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('admin.view_user', username=username))

@admin.route("/users/<username>/toggle_account_status")
@login_required
@admin_toggle_account_status.require(403)
def toggle_account_status(username):
    user = User.query.filter_by(username=username).first_or_404()
    user.active = not user.active
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('admin.view_user', username=username))