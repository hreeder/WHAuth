from flask import Blueprint
from flask.ext.principal import Permission, RoleNeed

admin = Blueprint("admin", __name__, template_folder="templates")

from auth import ACTIVE_ROLES
ACTIVE_ROLES.extend([
    'view-admin',

    'admin-view-users',
])

view_admin = Permission(RoleNeed('view-admin'))
admin_view_users = Permission(RoleNeed('admin-view-users'))

from auth.admin import views
from auth.admin.views import users