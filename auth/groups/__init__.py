from flask import Blueprint

groups = Blueprint('groups', __name__, template_folder='templates')

from auth.groups import models
from auth.groups.views import main