"""
Decorators that check for user permissions
"""
from functools import wraps
from flask import abort
from flask_login import current_user
from app.models.role import Permission
from flask import render_template


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                return render_template('403.html'), 403
                # abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
