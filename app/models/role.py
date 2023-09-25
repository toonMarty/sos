from app import db


class Permission:
    """
    Define Permissions for sos
    """
    CREATE_TICKET = 1
    SOLVE = 2
    ACCEPT = 4
    ESCALATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, permission):
        """
        Check if a user has certain permission(s)
        Example:
            self.permissions = 3 (011)
            the above statement means a user can create a ticket and solve
            the ticket 1 + 2 = 3
            Let's check if the user can accept tickets, 4(100)
            011 & 100 == 000. 000 translates to False, so the user doesn't have
            the accept ticket permission. The method returns False in this case
        Args:
            permission: the permission to check against
        """
        return self.permissions & permission == permission

    def add_permission(self, permission):
        """
        Grant a new permission to a particular user role
        Args:
            permission: the permission to grant/add
        """
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission):
        """
        Revoke a permission from a particular user
        Args:
            permission: the permission to revoke
        """
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        """
        Reset a users permission to the default value, 0
        """
        self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Novice': [Permission.CREATE_TICKET, Permission.ACCEPT],
            'Agent': [Permission.SOLVE, Permission.CREATE_TICKET, Permission.ESCALATE],
            'Administrator': [Permission.CREATE_TICKET, Permission.SOLVE,
                              Permission.ESCALATE, Permission.ACCEPT, Permission.ADMIN],
            'User': [Permission.CREATE_TICKET]
        }

        default_role = 'User'

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for permission in roles[r]:
                role.add_permission(permission)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return f'Role {self.name}'


