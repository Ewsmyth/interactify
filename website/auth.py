from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user
from .models import db, User, LogEvent, ALLOWED_EXTENSIONS, generate_unique_filename
from werkzeug.security import check_password_hash
import os

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        a1 = request.form.get('a2')  # Username or email
        b1 = request.form.get('b2')  # Password

        user = User.query.filter((User.email == a1) | (User.username == a1)).first()

        if user:
            if user.check_password(b1):  # Use check_password method here
                if user.acct_stat:
                    login_user(user)
                    if user.authority == 'admin':
                        return redirect(url_for('admin.adminhome', username=user.username))
                    elif user.authority == 'user':
                        return redirect(url_for('user.userhome', username=user.username))
                    else:
                        flash('Invalid Authority', 'error')
                        return redirect(url_for('auth.login'))
                else:
                    flash('Account is disabled, contact support', 'error')
                    return redirect(url_for('auth.login'))
            else:
                flash('Invalid password', 'error')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or email', 'error')
            return redirect(url_for('auth.login'))

    return render_template('authlogin.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        a1 = request.form.get('a2')  # Username
        b1 = request.form.get('b2')  # Email
        c1 = request.form.get('c2')  # Password
        d1 = request.form.get('d2')  # Confirm Password
        e1 = request.form.get('e2')  # First name
        f1 = request.form.get('f2')  # Last name
        g1 = request.files.get('g2')  # Profile picture

        if c1 != d1:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.signup'))

        # Check if username or email already exists
        existing_user = User.query.filter((User.username == a1) | (User.email == b1)).first()

        if existing_user:
            flash('Username or email is already registered with another account. Please choose a different one.', 'error')
            return redirect(url_for('auth.signup'))

        # Continue with user registration
        h1 = User(username=a1, email=b1, first_name=e1, last_name=f1)
        h1.set_password(c1)

        if g1 and g1.filename:  # Check if a file is selected
            # Generate a unique filename for the profile picture
            filename = generate_unique_filename(a1, g1.filename.rsplit('.', 1)[1].lower())

            # Save the file to the UPLOAD_FOLDER
            g1.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            # Set the profile_picture field in User model to the filename
            h1.profile_picture = filename

        db.session.add(h1)
        db.session.commit()

        event_description = f"New user '{a1}' has registered."
        new_event = LogEvent(event_description=event_description)
        db.session.add(new_event)
        db.session.commit()

        flash('Please login', 'success')
        return redirect(url_for('auth.login'))

    return render_template('authsignup.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))