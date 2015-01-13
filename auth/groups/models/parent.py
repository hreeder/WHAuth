from auth import db

class GroupParent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('group.id'))