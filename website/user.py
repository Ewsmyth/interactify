from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_from_directory
from .utils import userreq, current_user_has_liked
from flask_login import login_required, current_user
from .models import db, User, Post, Likes, Media, ALLOWED_EXTENSIONS, generate_unique_filename, Follower, LogEvent, Comment
from sqlalchemy import and_, or_, not_, desc
from sqlalchemy.sql.expression import func
import os

user = Blueprint('user', __name__)

@user.route('/<username>/userhome')
@login_required
@userreq
def userhome(username):
    # Fetch posts from the current user and the users they are following
    user_following = [follower.following_user for follower in current_user.following]
    user_following.append(current_user)  # Include the current user in the list

    a1 = Post.query.filter(
        and_(
            Post.archive == False,
            Post.author_id.in_([user.id for user in user_following])
        )
    ).limit(40).all()

    # Fetch liked status for each post for the current user
    c1 = {post.id: current_user_has_liked(post) for post in a1}

    # Fetch the count of likes for each post
    likes_count = {post.id: Likes.query.filter_by(liked_post=post.id).count() for post in a1}

    return render_template('userhome.html', username=username, a2=a1, c1=c1, likes_count=likes_count)

@user.route('/<username>/userpost', methods=['POST', 'GET'])
@login_required
@userreq
def userpost(username):
    if request.method == 'POST':
        a1 = request.form.get('a2')
        b1 = current_user

        # Check if both content and media files are empty after processing the form data
        media_files = request.files.getlist('media_files')

        media_urls = []  # to store unique media filenames

        for media_file in media_files:
            if media_file and '.' in media_file.filename and media_file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                unique_media_filename = generate_unique_filename(b1.username, media_file.filename.rsplit('.', 1)[1])
                media_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_media_filename))
                media_urls.append(unique_media_filename)

        c1 = Post(content=a1, author=b1)

        # Associate media files with the post
        for media_url in media_urls:
            new_media = Media(media_url=media_url, post=c1)
            db.session.add(new_media)

        db.session.add(c1)
        db.session.commit()

        event_description = f"{b1.username} posted {c1.content}."
        new_event = LogEvent(event_description=event_description)
        db.session.add(new_event)
        db.session.commit()

        flash('Post created', 'success')
        return redirect(url_for('user.userhome', username=username))

    return render_template('userpost.html', username=username)

@user.route('/<username>/userprofile')
@login_required
@userreq
def userprofile(username):
    user_to_display = User.query.filter_by(username=username).first()

    if user_to_display:
        posts = Post.query.filter(
            and_(
                Post.archive.is_(False),
                Post.author_id == user_to_display.id
            )
        ).all()

        for post in posts:
            print(f"Post {post.id} archive: {post.archive}")

        c1 = {post.id: current_user_has_liked(post) for post in posts}
        likes_count = {post.id: Likes.query.filter_by(liked_post=post.id).count() for post in posts}

        is_own_profile = current_user == user_to_display

        return render_template('userprofile.html', username=username, user_to_display=user_to_display, posts=posts, likes_count=likes_count, c1=c1, is_own_profile=is_own_profile)
    else:
        flash('User not found', 'error')
        return redirect(url_for('user.userhome', username=username))

@user.route('/<username>/usersearch', methods=['GET', 'POST'])
@login_required
@userreq
def usersearch(username):
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        users = User.query.filter(
            and_(
                User.username.ilike(f'%{search_term}%'),
                User.authority != 'admin'
            )
        ).all()
        return render_template('usersearch.html', username=username, users=users, search_term=search_term)

    # If no search term is provided, query for 20 random users in random order
    random_users = User.query.filter(User.authority != 'admin').order_by(func.random()).limit(20).all()

    return render_template('usersearch.html', username=username, users=random_users, search_term=None)

@user.route('/<username>/userprofile/usersettings')
@login_required
@userreq
def usersettings(username):
    a1 = User.query.filter_by(username=username).first()

    if not a1:
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))

    return render_template('usersettings.html', username=username, a1=a1)

@user.route('/<username>/userprofile/userstats')
@login_required
def userstats(username):
    user_to_display = User.query.filter_by(username=username).first()

    if user_to_display:
        followers = Follower.query.filter_by(following_id=user_to_display.id).all()
        following = Follower.query.filter_by(follower_id=user_to_display.id).all()

        return render_template('userstats.html', user_to_display=user_to_display, followers=followers, following=following)
    else:
        flash('User not found', 'error')
        return redirect(url_for('user.userhome', username=username))

################################

# Background routes

################################

@user.route('/like_post/<int:post_id>')
@login_required
@userreq
def like_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Get the primary key of the current user
    current_user_id = current_user.id

    # Check if the user has already liked the post
    if Likes.query.filter_by(liked_by=current_user_id, liked_post=post.id).first():
        # If liked, unlike
        Likes.query.filter_by(liked_by=current_user_id, liked_post=post.id).delete()
        liked = False
    else:
        # If not liked, like
        like = Likes(liked_by=current_user_id, liked_post=post.id)
        db.session.add(like)
        liked = True

    db.session.commit()

    # Fetch the count of likes for the specific post_id
    likes_count = Likes.query.filter_by(liked_post=post.id).count()

    # Return JSON response indicating whether the post is liked, and the updated like count
    return jsonify({'liked': liked, 'likes_count': likes_count})

@user.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
@userreq
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if current_user.id == post.author_id:
        # Soft delete: Set the 'archive' field to True
        post.archive = True

        event_description = f"{current_user.username} deleted post {post_id}."
        new_event = LogEvent(event_description=event_description)
        db.session.add(new_event)

        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Post deleted successfully.'})
    else:
        return jsonify({'status': 'error', 'message': 'You do not have permission to delete this post.'})

@user.route('/<username>/follow', methods=['POST'])
@login_required
@userreq
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()

    if user_to_follow:
        # Check if the current user is already following the user_to_follow
        existing_follower = Follower.query.filter_by(follower_id=current_user.id, following_id=user_to_follow.id).first()

        if existing_follower:
            # If already following, unfollow (delete the record)
            db.session.delete(existing_follower)
            flash('Unfollowed successfully', 'success')
        else:
            # If not following, follow (add a new record)
            new_follower = Follower(follower_id=current_user.id, following_id=user_to_follow.id)
            db.session.add(new_follower)
            flash('Followed successfully', 'success')

        db.session.commit()

        # Redirect back to the user profile page
        return redirect(url_for('user.userprofile', username=username))  # Use 'username' instead of 'username'
    else:
        flash('User not found', 'error')
        return redirect(url_for('user.userhome', username=username))

@user.route('/<username>/userprofile/usersettings/update_theme', methods=['POST'])
@login_required
@userreq
def update_theme(username):
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
    return redirect(url_for('user.usersettings', username=username))

@user.route('/<username>/userprofile/usersettings/user_change_bio', methods=['POST'])
@login_required
@userreq
def user_change_bio(username):
    a1 = request.form.get('a2')
    b1 = User.query.filter_by(bio=a1).first()

    if not a1:
        flash('Please provide a new bio', 'warning')
        return redirect(url_for('user.usersettings', username=username))

    current_user.bio = a1

    c1 = f"User {current_user.id} changed their bio."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Bio updated!', 'success')
    return redirect(url_for('user.usersettings', username=username))

@user.route('/<username>/userprofile/usersettings/user_change_username', methods=['POST'])
@login_required
@userreq
def user_change_username(username):
    a1 = request.form.get('a2')
    b1 = User.query.filter_by(username=a1).first()

    if not a1:
        flash('Please provide a new username', 'warning')
        return redirect(url_for('user.usersettings', username=username))

    if b1:
        flash('Username already exists. Please choose a different one.', 'warning')
        return redirect(url_for('user.usersettings', username=username))

    current_user.username = a1

    c1 = f"User {current_user.id} changed their username to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Username changed successfully!', 'success')
    return render_template('logout_timer.html')

@user.route('/<username>/userprofile/usersettings/user_change_email', methods=['POST'])
@login_required
@userreq
def user_change_email(username):
    a1 = request.form.get('a2')
    b1 = User.query.filter_by(email=a1).first()

    if not a1:
        flash('Please provide a new Email', 'warning')
        return redirect(url_for('user.usersettings', username=username))

    if b1:
        flash('Email is already used by another user', 'warning')
        return redirect(url_for('user.usersettings', username=username))

    current_user.email = a1

    c1 = f"{current_user.username} changed their email to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Email changed', 'success')
    return render_template('logout_timer.html')

@user.route('/<username>/userprofile/usersettings/user_change_password', methods=['POST'])
@login_required
@userreq
def user_change_password(username):
    a1 = request.form.get('a2') # Current password
    b1 = request.form.get('b2') # New password
    c1 = request.form.get('c2') # Confirm new password

    if not a1 or not b1 or not c1:
        flash('Please complete all password fields', 'warning')
        return redirect(url_for('user.usersettings', username=username))

    if b1 != c1:
        flash('Passwords do not match', 'error')
        return redirect(url_for('user.usersettings', username=username))

    if not current_user.check_password(a1):
        flash('Incorrect password', 'error')
        return redirect(url_for('user.usersettings', username=username))

    current_user.set_password(b1)

    d1 = f"{current_user.username} changed their password."
    e1 = LogEvent(event_description=d1)
    db.session.add(e1)

    db.session.commit()

    flash('Password changed successfully!', 'success')
    return render_template('logout_timer.html')

@user.route('/<username>/userprofile/usersettings/user_change_firstname', methods=['POST'])
@login_required
@userreq
def user_change_firstname(username):
    a1 = request.form.get('a2')

    current_user.first_name = a1

    c1 = f"{current_user.username} changed their first name to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('First name changed', 'success')
    return redirect(url_for('user.usersettings', username=username))

@user.route('/<username>/userprofile/usersettings/user_change_lastname', methods=['POST'])
@login_required
@userreq
def user_change_lastname(username):
    a1 = request.form.get('a2')

    current_user.last_name = a1

    c1 = f"{current_user.username} changed their last name to {a1}."
    d1 = LogEvent(event_description=c1)
    db.session.add(d1)

    db.session.commit()

    flash('Last name changed', 'success')
    return redirect(url_for('user.usersettings', username=username))

@user.route('/<username>/userprofile/usersettings/user_change_profile_picture', methods=['POST'])
@login_required
@userreq
def user_change_profile_picture(username):
    a1 = request.files.get('a2')

    if a1 and a1.filename:
        filename = generate_unique_filename(username, a1.filename.rsplit('.', 1)[1].lower())
        a1.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        current_user.profile_picture = filename

        db.session.commit()

        flash('Profile picture changed', 'success')
    else:
        flash('No file selected', 'error')

    return redirect(url_for('user.usersettings', username=username))

@user.route('/<username>/userprofile/usersettings/deactivate_account', methods=['POST'])
@login_required
@userreq
def deactivate_account(username):
    current_user.is_active = False

    event_description = f"{current_user.username} deactivated their account."
    new_event = LogEvent(event_description=event_description)
    db.session.add(new_event)

    db.session.commit()

    # You might want to handle additional cleanup or logic here
    flash('Your account has been deactivated')
    return redirect(url_for('auth.logout'))

@user.route('/<username>/upload_comment/<int:post_id>', methods=['POST'])
@login_required
@userreq
def upload_comment(username, post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        comment_content = request.form.get('comment_content')

        if comment_content:
            new_comment = Comment(content=comment_content, post=post, comment_user=current_user)
            db.session.add(new_comment)
            db.session.commit()
            likes_count = Comment.query.filter_by(post_id=post.id).count()
            return jsonify({'message': 'Comment added successfully!', 'status': 'success', 'likes_count': likes_count})
        else:
            return jsonify({'message': 'Comment content cannot be empty.', 'status': 'danger'})

    return jsonify({'message': 'Invalid request.', 'status': 'danger'})
