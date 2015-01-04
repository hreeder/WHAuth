import os

from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.login import LoginManager

from auth.core import core

app = Flask(__name__)
app.config.from_object("config")

# Load Blueprints
app.register_blueprint(core)

# Load Extensions
assets = Environment(app)
login_manager = LoginManager(app)

# Configure flask-login
login_manager.login_view = "core.login"

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