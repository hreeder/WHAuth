#
# groups/views/main.py
# Contains view methods for all normal user interactions with groups
#

from flask import render_template, redirect, url_for
from flask.ext.login import login_required

from auth.groups import groups
from auth.groups.models import Group, GroupCategory

@groups.route("/")
@login_required
def list_own():
    return render_template(
        'groups/list_own.html'
    )

@groups.route("/available")
@login_required
def list_available():
    all_categories = GroupCategory.query.all()
    categories = []

    for category in all_categories:
        show = False
        groups = []
        for group in category.groups.order_by(Group.name).all():
            if group.visible:
                show = True
                groups.apend()
    return render_template(
        'groups/list_available.html',
    )