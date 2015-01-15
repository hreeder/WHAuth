#
# groups/views/admin.py
# Contains view methods for group leader administration
#
import datetime

from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user

from auth import db

from auth.groups import groups
from auth.groups.models import Group, GroupMembership

@groups.route("/<groupid>/admin")
@login_required
def admin(groupid):
    group = Group.query.filter_by(id=groupid).first_or_404()

    if not group.is_user_admin(current_user):
        flash("You are not an admin of that group.", "danger")
        return redirect(url_for('groups.list_own'))

    pending = GroupMembership.query.filter_by(group_id=group.id, app_pending=True).all()
    members = GroupMembership.query.filter_by(group_id=group.id, app_pending=False).all()

    return render_template(
        'groups/admin.html',
        group=group,
        pending=pending,
        members=members
    )

@groups.route("/<groupid>/admin/<appid>/accept")
@login_required
def accept_app(groupid, appid):
    group = Group.query.filter_by(id=groupid).first_or_404()

    if not group.is_user_admin(current_user):
        flash("You are not an admin of that group.", "danger")
        return redirect(url_for('groups.list_own'))

    app = GroupMembership.query.filter_by(id=appid, app_pending=True).first_or_404()
    app.app_pending=False
    app.last_updated=datetime.datetime.utcnow()

    db.session.add(app)
    db.session.commit()

    flash('The application to %s by %s has been accepted' % (app.group.name, app.user.get_display_name()), 'success')
    return redirect(url_for('groups.admin', groupid=groupid))

@groups.route("/<groupid>/admin/<appid>/reject")
@login_required
def reject_app(groupid, appid):
    group = Group.query.filter_by(id=groupid).first_or_404()

    if not group.is_user_admin(current_user):
        flash("You are not an admin of that group.", "danger")
        return redirect(url_for('groups.list_own'))

    app = GroupMembership.query.filter_by(id=appid, app_pending=True).first_or_404()

    db.session.delete(app)
    db.session.commit()

    flash('The application to %s by %s has been rejected' % (app.group.name, app.user.get_display_name()), 'danger')
    return redirect(url_for('groups.admin', groupid=groupid))


@groups.route("/<groupid>/admin/<appid>/kick")
@login_required
def kick_member(groupid, appid):
    group = Group.query.filter_by(id=groupid).first_or_404()

    if not group.is_user_admin(current_user):
        flash("You are not an admin of that group.", "danger")
        return redirect(url_for('groups.list_own'))

    app = GroupMembership.query.filter_by(id=appid, app_pending=False).first_or_404()

    db.session.delete(app)
    db.session.commit()

    flash('%s has been removed from the group %s' % (app.user.get_display_name(), app.group.name), 'danger')
    return redirect(url_for('groups.admin', groupid=groupid))