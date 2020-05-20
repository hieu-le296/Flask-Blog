#socialblog/__init__.py

import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'

from flask_dance.contrib.google import make_google_blueprint, google
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import sqlalchemy_utils
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_dance.contrib.google import make_google_blueprint, google


app = Flask(__name__)

app.config['SECRET_KEY'] = 'myscecret'


##################
####Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)


app.config['UPLOADS_DEFAULT_DEST'] = TOP_LEVEL_DIR + '/socialblog/static/posts/'
app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/static/posts/'
app.config['UPLOADED_IMAGES_DEST'] = TOP_LEVEL_DIR + '/socialblog/static/posts/'
app.config['UPLOADED_IMAGES_URL'] = 'http://localhost:5000/static/posts/'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
                DEBUG = True,
                # Email Setting
                MAIL_SERVER = 'smtp.gmail.com',
                MAIL_PORT = 465,
                MAIL_USE_SSL = True,
                MAIL_USERNAME = 'techtalks.flaskblog@gmail.com',
                MAIL_PASSWORD = 'ialyqgyukhwbbnjn',
)

oauth_blueprint = make_google_blueprint(client_id='658744636791-4mrjk59uti6hefkv99tuqgb9vfj7c4mr.apps.googleusercontent.com',
                                        client_secret='iWTt-jNLq5VXjJa3pqILhP1v',
                                        offline=True, scope=["profile", "email"],
                                        redirect_to='users.register_google'
                                        )

db = SQLAlchemy(app)
Migrate(app, db)

##################
####Login Config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

##################
####Mail Config
mail = Mail(app)


# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

from socialblog.core.views import core
from socialblog.users.views import users
from socialblog.users.views import oauth_blueprint
from socialblog.blog_posts.views import blog_posts
from socialblog.error_pages.handler import error_pages
from socialblog.comments.views import user_comments

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)
app.register_blueprint(oauth_blueprint, url_prefix='/login')
app.register_blueprint(user_comments)