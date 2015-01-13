from auth import db
from auth.groups.models.parent import GroupParent

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('group_category.id'))
    visible = db.Column(db.Boolean)
    open = db.Column(db.Boolean)
    leavable = db.Column(db.Boolean)

    parents = db.relationship('GroupParent', backref='group', lazy='dynamic', foreign_keys=[GroupParent.group_id])

    def visible_to(self, user):
        if not self.visible:
            return False