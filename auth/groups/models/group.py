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

    @property
    def parents(self):
        return [parent.parent for parent in GroupParent.query.filter_by(group_id=self.id).all()]

    @property
    def children(self):
        return [child.group for child in GroupParent.query.filter_by(parent_id=self.id).all()]

    def visible_to(self, user):
        if not self.visible:
            return False