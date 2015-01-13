from auth import db

class GroupParent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    @property
    def parent(self):
        from auth.groups.models.group import Group
        return Group.query.filter_by(id=self.parent_id).first()

    @property
    def group(self):
        from auth.groups.models.group import Group
        return Group.query.filter_by(id=self.group_id).first()