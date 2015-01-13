from auth import db
from auth.groups.models.membership import GroupMembership
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

    @property
    def members(self):
        return [membership.user for membership in GroupMembership.query.filter_by(group_id=self.id).all()]

    def visible_to(self, user):
        # Superusers see all groups
        # TODO: Expand to accomodate roles system
        if user.superuser:
            return True

        # If the group isn't visible then return False
        if not self.visible:
            return False

        # If there aren't any parents, this is a top level group and thus is visible to any user
        if not self.parents:
            return True

        # Make a set of group IDs for valid parents, and for groups the user is currently a member of
        parent_ids = set([int(parent.id) for parent in self.parents])
        user_group_ids = set([int(group.id) for group in user.groups])

        # Return True/False if there is an intersection between those sets
        # True means there is an intersection, and thus the user can see this group
        # False / No Intersection means the user is not in any valid parent groups
        return bool(parent_ids & user_group_ids)