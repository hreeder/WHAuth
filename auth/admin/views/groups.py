from flask import render_template, redirect, url_for
from flask.ext.login import login_required
from sqlalchemy import asc

from auth import db
from auth.admin import admin, admin_view_groups, admin_create_groups, admin_create_group_categories
from auth.admin.forms.groups import NewGroupForm, NewCategoryForm
from auth.groups.models import Group, GroupCategory, GroupParent
from auth.utils import flash_errors

@admin.route("/groups")
@login_required
@admin_view_groups.require(403)
def list_groups():
    groups = Group.query.all()
    return render_template(
        'admin/groups/list_groups.html',
        groups=groups
    )

@admin.route("/groups/new", methods=['GET', 'POST'])
@login_required
@admin_create_groups.require(403)
def add_group():
    form = NewGroupForm()
    form.category.choices = [(c.id, c.name) for c in GroupCategory.query.order_by(asc(GroupCategory.order)).all()]
    form.parents.choices = [(g.id, g.name) for g in Group.query.order_by(asc(Group.name)).all()]

    if form.validate_on_submit():
        group = Group()
        group.name = form.name.data
        group.description = form.description.data
        group.category_id = form.category.data
        group.visible = form.visible.data
        group.open = form.open.data
        group.leavable = form.leavable.data

        db.session.add(group)
        db.session.commit()

        # create parents
        for parent_id in form.parents.data:
            parent = GroupParent(
                group_id=group.id,
                parent_id=parent_id
            )
            db.session.add(parent)

        db.session.commit()

        return redirect(url_for('admin.list_groups'))
    else:
        flash_errors(form)

    return render_template(
        'admin/groups/add_group.html',
        form=form
    )

@admin.route("/groups/categories")
@login_required
@admin_view_groups.require(403)
def list_group_categories():
    categories = GroupCategory.query.all()
    return render_template(
        'admin/groups/list_categories.html',
        categories=categories
    )

@admin.route("/groups/categories/new", methods=['GET', 'POST'])
@login_required
@admin_create_group_categories.require(403)
def add_group_category():
    form = NewCategoryForm()
    if form.validate_on_submit():
        category = GroupCategory()
        category.name = form.name.data
        category.order = form.order.data

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.list_group_categories'))
    else:
        flash_errors(form)
    return render_template(
        'admin/groups/add_category.html',
        form=form
    )