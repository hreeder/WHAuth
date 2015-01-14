from flask_wtf import Form
from wtforms import TextAreaField

class ApplyToGroupForm(Form):
    reason = TextAreaField('Reason')