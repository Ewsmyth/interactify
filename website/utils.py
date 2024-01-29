import os
from flask import Blueprint, redirect, url_for, flash, send_from_directory
from .models import db, User, Likes
from functools import wraps
from flask_login import current_user

utils = Blueprint('utils', __name__)

# The adminreq function can be used as a route decorator to restrict access to any user other than an admin
def adminreq(l22):
    @wraps(l22)
    def l33(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        elif current_user.authority != 'admin':
            flash('You do not have permission to access this page')
            return redirect(url_for('auth.logout'))
        return l22(*args, **kwargs)
    return l33

# The userreq function can be used as a route decorator to restrict access to any user other than a user
def userreq(l22):
    @wraps(l22)
    def l33(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        elif current_user.authority != 'user':
            flash('You dont have permission to access this page')
            return redirect(url_for('auth.logout'))
        return l22(*args, **kwargs)
    return l33

def current_user_has_liked(post):
    return Likes.query.filter_by(liked_by=current_user.id, liked_post=post.id).first() is not None

@utils.route('/staticp/<path:filename>')
def staticp(filename):
    static_folder = os.path.join(os.getcwd(), 'website')
    return send_from_directory(static_folder, filename)

