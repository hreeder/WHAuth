import os

from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.login import LoginManager, current_user
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.principal import Principal, identity_loaded, RoleNeed

app = Flask(__name__)
app.config.from_object("config")

# Load Extensions
assets = Environment(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
principals = Principal(app)

ACTIVE_ROLES = []

# Optional Extensions
if app.config['EMAIL_METHOD'].lower() == "smtp":
    from flask.ext.mail import Mail
    mail = Mail(app)

# Load Blueprints
from auth.admin import admin
from auth.core import core

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(core)

# Configure flask-login
login_manager.login_view = "core.login"

# Load permissions
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if current_user.is_anonymous():
        return False

    if current_user.superuser:
        for role in ACTIVE_ROLES:
            identity.provides.add(RoleNeed(role))

# Assets Setup
assets.load_path.append(os.path.join(os.path.dirname(__file__), 'static', 'bower'))

assets.register(
    'js_all',
    Bundle(
        'jquery/dist/jquery.min.js',
        'bootstrap/dist/js/bootstrap.min.js',
        output='js_all.js'
    )
)

assets.register(
    'css_all',
    Bundle(
        'bootstrap/dist/css/bootstrap.css',
        'bootstrap-material-design/dist/css/material.css',
        'bootstrap-material-design/dist/css/material-wfont.css',
        'bootstrap-material-design/dist/css/ripples.css',
        filters='cssmin',
        output='css_all.css'
    )
)