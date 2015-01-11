from auth import db

class GroupCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    order = db.Column(db.Integer)
    groups = db.relationship('Group', backref='category', lazy='dynamic')