from auth import db

class GroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group_admin = db.Column(db.Boolean)
    app_pending = db.Column(db.Boolean)
    app_text = db.Column(db.Text)

    @property
    def user(self):
        from auth.core.models.user import User
        return User.query.filter_by(id=self.member_id).first()

    @property
    def group(self):
        from auth.groups.models.group import Group
        return Group.query.filter_by(id=self.group_id).first()