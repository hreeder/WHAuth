from flask import render_template
from flask.ext.login import login_required

from auth.admin import admin, view_admin
from auth.core.models.user import User

@admin.route("/")
@login_required
@view_admin.require(403)
def dashboard():
    all_users = User.query.all()
    return render_template(
        "admin/dashboard.html",
        user_count=len(all_users)
    )