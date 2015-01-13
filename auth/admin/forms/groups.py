from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, SelectMultipleField
from wtforms.validators import InputRequired

class NewGroupForm(Form):
    name = StringField('Group Name', validators=[InputRequired()])
    description = TextAreaField('Description')
    category = SelectField('Category', coerce=int)
    visible = BooleanField('Group Visible')
    open = BooleanField('Group Open')
    leavable = BooleanField('Group Leavable')
    parents = SelectMultipleField('Parent Group(s)', coerce=int)


class NewCategoryForm(Form):
    name = StringField('Category Name', validators=[InputRequired()])
    order = IntegerField('Order Value', validators=[InputRequired()])