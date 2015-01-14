#
# groups/views/main.py
# Contains view methods for all normal user interactions with groups
#

from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from sqlalchemy import asc

from auth import db
from auth.utils import flash_errors

from auth.groups import groups
from auth.groups.models import Group, GroupCategory, GroupMembership
from auth.groups.forms import ApplyToGroupForm

@groups.route("/")
@login_required
def list_own():
    return render_template(
        'groups/list_own.html'
    )

@groups.route("/available")
@login_required
def list_available():
    all_categories = GroupCategory.query.order_by(asc(GroupCategory.order)).all()
    categories = []

    for category in all_categories:
        show = False
        groups = []
        for group in category.groups.order_by(Group.name).all():
            if group.visible_to(current_user):
                show = True
                groups.append(group)

        if show:
            categories.append({
                'name': category.name,
                'order': category.order,
                'groups': groups
            })
    return render_template(
        'groups/list_available.html',
        categories=categories
    )

@groups.route('/apply/<groupid>', methods=['GET', 'POST'])
@login_required
def apply(groupid):
    # Find Group
    group = Group.query.filter_by(id=groupid).first_or_404()
    # Check if user is already in group
    member = GroupMembership.query.filter_by(member_id=current_user.id, group_id=group.id).first()

    if not group.joinable_for(current_user):
        flash("You are ineligible to apply to that group at the current time.", "danger")
        return redirect(url_for('groups.list_available'))

    if member:
        if member.app_pending:
            flash("You already have a pending application to that group, you cannot submit a second one.", "danger")
        else:
            flash("You are already a member of that group, you cannot join a second time", "danger")
        return redirect(url_for("groups.list_available"))

    form = ApplyToGroupForm()

    if form.validate_on_submit():
        membership = GroupMembership(
            member_id=current_user.id,
            group_id=group.id,
            group_admin=False,
            app_pending=True,
            app_text=form.reason.data,
        )

        db.session.add(membership)
        db.session.commit()

        # TODO: Email group admins

        flash("Your application has been submitted and the group admins notified. "
              "You will receive a notification when your application has been reviewed.",
              'success')
        return redirect(url_for('groups.list_own'))
    else:
        flash_errors(form)

    return render_template(
        'groups/apply.html',
        group=group,
        form=form
    )