from flask import render_template
from flask.ext.login import login_required

from auth.admin import admin, admin_view_users
from auth.core.models.user import User

@admin.route("/users")
@login_required
@admin_view_users.require(403)
def list_users():
    all = User.query.all()
    admins = User.query.filter_by(superuser=True).all()

    return render_template(
        "admin/users/list.html",
        all_users=all,
        admins=admins
    )