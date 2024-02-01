from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()
bcrypt = Bcrypt()
ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'jpeg', 'gif', 'mp4'}

# This decorator generates a unique filename
def generate_unique_filename(username, file_extension):
    current_time = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    random_digits = str(uuid.uuid4().int & (1 << 32) - 1).zfill(5)
    return f"{username}_{current_time}_{random_digits}.{file_extension}"

class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    authority = db.Column(db.String(20), nullable=False, default='user')
    theme = db.Column(db.Boolean(), default=False)
    acct_stat = db.Column(db.Boolean(), nullable=False, default=True)
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships for followers
    followers = db.relationship('Follower', foreign_keys=[Follower.following_id], backref=db.backref('following_user', lazy='joined'), lazy='dynamic')

    following = db.relationship('Follower', foreign_keys=[Follower.follower_id], backref=db.backref('follower_user', lazy='joined'), lazy='dynamic')

    posts = db.relationship('Post', backref='author', lazy=True)
    liker = db.relationship('Likes', backref='liker_user', lazy=True)
    comments = db.relationship('Comment', backref='comment_user', lazy=True)

    def is_following(self, user):
        return Follower.query.filter_by(follower_id=self.id, following_id=user.id).first() is not None

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8') if not isinstance(generate_password_hash(password), str) else generate_password_hash(password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(800))
    archive = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    liked_posts = db.relationship('Likes', backref='post_id', lazy=True)
    media = db.relationship('Media', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def is_allowed_extension(self, file_extension):
        return file_extension.lower() in ALLOWED_EXTENSIONS

    def generate_unique_filename(self, file_extension):
        if self.is_allowed_extension(file_extension):
            return generate_unique_filename(self.author.username, file_extension)
        else:
            raise ValueError("File extension not allowed")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(800))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_url = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    liked_post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LogEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)