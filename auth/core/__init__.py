from flask import Blueprint

core = Blueprint('core', __name__, template_folder='templates')
import auth.core.views

from auth.core.models import user