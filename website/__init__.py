from flask import Flask
from flask_login import LoginManager
from .models import db, User

def create_app():
    app = Flask(__name__, static_folder='/var/lib/docker/volumes/interactify-uploads', static_url_path='/uploads')

    app.config['UPLOAD_FOLDER'] = '/var/lib/docker/volumes/interactify-uploads'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/lib/docker/volumes/interactify-data/interactify-data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'aabbccddeeffgg'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from .auth import auth
    from .admin import admin
    from .user import user
    from .utils import utils
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(utils)

    # The ya22 function is called when the server is initialized and it creates an admin user if one does not already exist
    def ya222():
        a1 = User.query.filter_by(authority='admin').first()
        if not a1:
            a1 = User(
                username='admin',
                email='admin@admin.com',
                first_name='admin',
                last_name='admin',
                authority='admin',
            )
            a1.set_password('password')
            db.session.add(a1)
            db.session.commit()
            print("Admin user created successfully")

    with app.app_context():
        db.create_all()
        ya222()
    
    return app
