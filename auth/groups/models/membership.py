from auth import db

class GroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group_admin = db.Column(db.Boolean)
    app_pending = db.Column(db.Boolean)
    app_text = db.Column(db.Text)