from flask import Blueprint, render_template, redirect, flash, url_for, request
from .utils import adminreq
from flask_login import login_required, current_user
from .models import db, User, LogEvent

admin = Blueprint('admin', __name__)

@admin.route('/<username>/adminhome')
@login_required
@adminreq
def adminhome(username):
    return render_template('adminhome.html', username=username)

@admin.route('/<username>/adminhome/adminusers', methods=['GET', 'POST'])
@login_required
@adminreq
def adminusers(username):
    if request.method == 'POST':
        # Form submitted, handle search
        field = request.form.get('field')
        keyword = request.form.get('keyword')

        # Perform the search based on the selected field and keyword
        # You need to adapt this part based on your specific search criteria
        if field and keyword:
            users = User.query.filter(getattr(User, field).ilike(f"%{keyword}%")).all()
        else:
            # Handle case where either field or keyword is missing
            users = User.query.all()

        return render_template('adminusers.html', username=username, users=users, User=User)

    # Render the page without search results for initial load
    return render_template('adminusers.html', username=username, User=User)

@admin.route('/<username>/adminhome/adminusers/adminedituser', methods=['GET', 'POST'])
@login_required
@adminreq
def adminedituser(username):
    user_to_edit = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        # Handle form submission to update username, password, and authority
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        new_authority = request.form.get('new_authority')

        # Update the user's username, password, and authority
        user_to_edit.username = new_username
        user_to_edit.set_password(new_password)
        user_to_edit.authority = new_authority

        # Commit changes to the database
        event_description = f"{current_user.username} updated {user_to_edit.username}'s account."
        new_event = LogEvent(event_description=event_description)
        db.session.add(new_event)
        db.session.commit()

        flash('User information updated successfully', 'success')
        return redirect(url_for('admin.adminusers', username=username))

    return render_template('adminedituser.html', username=username, user=user_to_edit)

@admin.route('/<username>/adminhome/admincreateuser', methods=['GET', 'POST'])
@login_required
@adminreq
def admincreateuser(username):
    if request.method == 'POST':
        a1 = request.form.get('a2') # Username
        b1 = request.form.get('b2') # Email
        c1 = request.form.get('c2') # Password
        d1 = request.form.get('d2') # Authority
        e1 = "Fistname"
        f1 = "Lastname"
        username = current_user.username

        g1 = User(
            username=a1, 
            email=b1,
            authority=d1, 
            first_name=e1, 
            last_name=f1)
        g1.set_password(c1)
        db.session.add(g1)

        h1 = f"{current_user.username} created user {a1}."
        i1 = LogEvent(event_description=h1)
        db.session.add(i1)

        db.session.commit()

        flash('New user created', 'success')
        return redirect(url_for('admin.admincreateuser', username=request.form.get('a2')))

    return render_template('admincreateuser.html', username=username)

@admin.route('/<username>/adminhome/adminprofile')
@login_required
@adminreq
def adminprofile(username):
    a1 = User.query.filter_by(username=username).first()

    if not a1:
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))

    return render_template('adminprofile.html', username=username, a1=a1)

@admin.route('/<username>/adminhome/adminlogs')
@login_required
@adminreq
def adminlogs(username):
    log_events = LogEvent.query.order_by(LogEvent.timestamp.desc()).limit(60).all()
    return render_template('adminlogs.html', username=username, log_events=log_events)

@admin.route('/<username>/adminprofile/adminupdate_theme', methods=['POST'])
@login_required
@adminreq
def adminupdate_theme(username):
    a1 = User.query.filter_by(username=username).first()

    if not a1:
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))

    b1 = request.form.get('b2')

    if b1 == '1':
        a1.theme = True
    else:
        a1.theme = False

    db.session.commit()

    flash('Theme update successfully', 'success')
    return redirect(url_for('admin.adminprofile', username=username))

@admin.route('/<username>/adminprofile/admin_change_username', methods=['POST'])
@login_required
@adminreq
def admin_change_username(username):
    a1 = request.form.get('a2')
    b1 = User.query.filter_by(username=a1).first()

    if not a1:
        flash('Please provide a new username', 'warning')
        return redirect(url_for('admin.adminprofile', username=username))

    if b1:
        flash('Username is already used by another user', 'warning')
        return redirect(url_for('admin.adminprofile', username=username))

    current_user.username = a1

    c1 = f"Admin user {current_user.id} changed their username to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Username changed', 'success')
    return render_template('logout_timer.html')

@admin.route('/<username>/adminprofile/admin_change_email', methods=['POST'])
@login_required
@adminreq
def admin_change_email(username):
    a1 = request.form.get('a2')
    b1 = User.query.filter_by(email=a1).first()

    if not a1:
        flash('Please provide a new Email', 'warning')
        return redirect(url_for('admin.adminprofile', username=username))

    if b1:
        flash('Email is already used by another user', 'warning')
        return redirect(url_for('admin.adminprofile', username=username))

    current_user.email = a1

    c1 = f"Admin user {current_user.username} changed their email to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Email changed', 'success')
    return render_template('logout_timer.html')

@admin.route('/<username>/adminprofile/admin_change_password', methods=['POST'])
@login_required
@adminreq
def admin_change_password(username):
    a1 = request.form.get('a2') # Current password
    b1 = request.form.get('b2') # New password
    c1 = request.form.get('c2') # Confirm new password

    if not a1 or not b1 or not c1:
        flash('Please complete all password fields', 'warning')
        return redirect(url_for('admin.adminprofile', username=username))

    if b1 != c1:
        flash('Passwords do not match', 'error')
        return redirect(url_for('admin.adminprofile', username=username))

    if not current_user.check_password(a1):
        flash('Incorrect password', 'error')
        return redirect(url_for('admin.adminprofile', username=username))

    current_user.set_password(b1)

    d1 = f"Admin user, {current_user.username} changed their password"
    e1 = LogEvent(event_description=d1)
    db.session.add(e1)

    db.session.commit()

    flash('Password Changed successfully', 'success')
    return render_template('logout_timer.html')

@admin.route('/<username>/adminprofile/admin_change_firstname', methods=['POST'])
@login_required
@adminreq
def admin_change_firstname(username):
    a1 = request.form.get('a2')

    current_user.first_name = a1

    c1 = f"Admin user {current_user.username} changed their First Name to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('First name changed', 'success')
    return redirect(url_for('admin.adminprofile', username=username))

@admin.route('/<username>/adminprofile/admin_change_lastname', methods=['POST'])
@login_required
@adminreq
def admin_change_lastname(username):
    a1 = request.form.get('a2')

    current_user.last_name = a1

    c1 = f"Admin user {current_user.username} changed their Last Name to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Last name changed', 'success')
    return redirect(url_for('admin.adminprofile', username=username))
