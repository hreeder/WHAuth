from flask import render_template
from flask.ext.login import login_required

from auth.admin import admin, admin_view_groups
from auth.groups.models import Group

@admin.route("/groups")
@login_required
@admin_view_groups.require(403)
def list_groups():
    groups = Group.query.all()
    return render_template(
        'admin/groups/list_groups.html',
        groups=groups
    )