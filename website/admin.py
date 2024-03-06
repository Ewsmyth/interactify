from flask import Blueprint, render_template, redirect, flash, url_for, request
from .utils import adminreq
from flask_login import login_required, current_user
from .models import db, User, LogEvent, Post, Likes, Comment, Media
from sqlalchemy import desc
import os

admin = Blueprint('admin', __name__)

@admin.route('/<username>/adminhome')
@login_required
@adminreq
def adminhome(username):
    # Count of users with authority=admin
    a1 = User.query.filter_by(authority='admin').count() # Admin user count

    # Count of users with authority=user
    b1 = User.query.filter_by(authority='user').count() # User count

    # Total number of posts
    c1 = Post.query.count() # Total post count

    # Total number of media files
    d1 = Media.query.count() # Media files count

    # Total number of likes
    e1 = Likes.query.count() # Total likes count

    # Total number of comments
    f1 = Comment.query.count() # Total comments count

    return render_template('adminhome.html', username=username, a1=a1, b1=b1, c1=c1, d1=d1, e1=e1, f1=f1)

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

@admin.route('/<username>/adminhome/adminusers/adminedituser/<int:user_id>', methods=['GET', 'POST'])
@login_required
@adminreq
def adminedituser(username, user_id):
    user_to_edit = User.query.get_or_404(user_id)

    return render_template('adminedituser.html', username=username, user_to_edit=user_to_edit)

@admin.route('/<username>/adminhome/admincreateuser', methods=['GET', 'POST'])
@login_required
@adminreq
def admincreateuser(username):
    if request.method == 'POST':
        a1 = request.form.get('a2')  # Username
        b1 = request.form.get('b2')  # Email
        c1 = request.form.get('c2')  # Password
        d1 = request.form.get('d2')  # Authority
        e1 = "Firstname"
        f1 = "Lastname"
        username = current_user.username

        # Check if username or email is already in use
        existing_user = User.query.filter((User.username == a1) | (User.email == b1)).first()

        if existing_user:
            flash('Username or email is already in use by another user.', 'error')
            return render_template('admincreateuser.html', username=username)

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
    log_events = LogEvent.query.filter_by(status=False).order_by(LogEvent.timestamp.desc()).limit(60).all()
    return render_template('adminlogs.html', username=username, log_events=log_events)

@admin.route('/<username>/adminhome/admintotalposts')
@login_required
@adminreq
def admintotalposts(username):
    post = Post.query.order_by(desc(Post.updated_at)).all()

    return render_template('admintotalposts.html', username=username, post=post)

@admin.route('/<username>/adminhome/adminsweep')
@login_required
@adminreq
def adminsweep(username):
    return render_template('adminsweep.html', username=username)

@admin.route('/sweep_media', methods=['GET', 'POST'])
@login_required
@adminreq
def sweep_media():
    # Get all media URLs from the database
    media_urls = [media.media_url for media in Media.query.all()]

    # Get all files in the uploads folder
    uploads_folder = 'D:/interactify-uploads'
    all_files = os.listdir(uploads_folder)

    # Iterate over files in the uploads folder
    for file in all_files:
        # If the file is not in the list of media URLs, delete it
        if file not in media_urls:
            os.remove(os.path.join(uploads_folder, file))

    flash("Sweep operation completed successfully.")
    return redirect(url_for('admin.adminsweep', username=current_user.username))

@admin.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
@adminreq
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Delete associated comments
    for comment in post.comments:
        db.session.delete(comment)
    # Delete associated likes
    for like in post.liked_posts:
        db.session.delete(like)
    # Delete associated media records
    for media in post.media:
        db.session.delete(media)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin.admintotalposts', username=current_user.username))

@admin.route('/delete_all_posts', methods=['POST'])
@login_required
@adminreq
def delete_all_posts():
    if request.method == 'POST':
        # Delete all posts
        posts = Post.query.all()
        for post in posts:
            # Delete associated comments
            for comment in post.comments:
                db.session.delete(comment)
            # Delete associated likes
            for like in post.liked_posts:
                db.session.delete(like)
            # Delete associated media records
            for media in post.media:
                db.session.delete(media)
            db.session.delete(post)
        db.session.commit()
        flash("All posts deleted successfully")
        return redirect(url_for('admin.admintotalposts', username=current_user.username))
    else:
        # Handle other methods (GET, etc.)
        return "Method Not Allowed", 405
    
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

    c1 = f"Admin {current_user.username} changed their email to {a1}."
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

    d1 = f"Admin {current_user.username} changed their password."
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

    c1 = f"Admin {current_user.username} changed their first name to {a1}."
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

    c1 = f"Admin {current_user.username} changed their last name to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Last name changed', 'success')
    return redirect(url_for('admin.adminprofile', username=username))

@admin.route('/<username>/adminhome/update_log_event_status/<int:log_event_id>', methods=['POST'])
@login_required
@adminreq
def update_log_event_status(username, log_event_id):
    log_event = LogEvent.query.get_or_404(log_event_id)
    log_event.status = request.form.get('status') == 'True'
    db.session.commit()
    flash(f'Status updated for log event with ID {log_event.id}', 'success')
    return redirect(url_for('admin.adminlogs', username=username))

@admin.route('/<username>/adminhome/adminusers/admineditusername', methods=['POST'])
@login_required
@adminreq
def admineditusername(username):
    user_to_edit = User.query.filter_by(username=username).first()

    if not user_to_edit:
        flash('User not found', 'error')
        return redirect(url_for('admin.adminusers', username=username))

    new_username = request.form.get('new_username')
    user_to_edit.username = new_username

    event_description = f"{current_user.username} updated {user_to_edit.username}'s username."
    new_event = LogEvent(event_description=event_description)
    db.session.add(new_event)
    db.session.commit()

    flash('Username updated successfully', 'success')
    return redirect(url_for('admin.adminedituser', username=user_to_edit.username, user_id=user_to_edit.id))

@admin.route('/<username>/adminhome/adminusers/admineditpassword', methods=['POST'])
@login_required
@adminreq
def admineditpassword(username):
    user_to_edit = User.query.filter_by(username=username).first()

    new_password = request.form.get('new_password')
    user_to_edit.set_password(new_password)

    event_description = f"{current_user.username} updated {user_to_edit.username}'s password."
    new_event = LogEvent(event_description=event_description)
    db.session.add(new_event)
    db.session.commit()

    flash('Password updated successfully', 'success')
    return redirect(url_for('admin.adminedituser', username=user_to_edit.username, user_id=user_to_edit.id))

@admin.route('/<username>/adminhome/adminusers/admineditauthority', methods=['POST'])
@login_required
@adminreq
def admineditauthority(username):
    user_to_edit = User.query.filter_by(username=username).first()

    new_authority = request.form.get('new_authority')
    user_to_edit.authority = new_authority

    event_description = f"{current_user.username} updated {user_to_edit.username}'s authority."
    new_event = LogEvent(event_description=event_description)
    db.session.add(new_event)
    db.session.commit()

    flash('Authority updated successfully', 'success')
    return redirect(url_for('admin.adminedituser', username=user_to_edit.username, user_id=user_to_edit.id))

@admin.route('/<username>/adminhome/adminusers/admineditstatus', methods=['POST'])
@login_required
@adminreq
def admineditstatus(username):
    user_to_edit = User.query.filter_by(username=username).first()

    new_acct_stat = request.form.get('new_acct_stat')
    user_to_edit.acct_stat = new_acct_stat == 'True'

    event_description = f"{current_user.username} updated {user_to_edit.username}'s status."
    new_event = LogEvent(event_description=event_description)
    db.session.add(new_event)
    db.session.commit()

    flash('Status updated successfully', 'success')
    return redirect(url_for('admin.adminedituser', username=user_to_edit.username, user_id=user_to_edit.id))
