# models.py
from socialblog import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
import sqlalchemy_utils
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, session, request


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(64), nullable=False, default='default.png')
    profile_cover = db.Column(
        db.String(64), nullable=False, default='default_cover.jpg')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author',
                            lazy=True, cascade="all, delete, delete-orphan")

    comments = db.relationship('Comments', backref='author',
                               lazy=True, cascade="all, delete, delete-orphan")


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'Username: {self.username}; Email: {self.email}'

class BlogPost(db.Model):
    __tablename__ = 'blogposts'
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    comments = db.relationship('Comments', backref='post',
                               lazy=True, cascade="all, delete, delete-orphan")
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)

    def __init__(self, title, text, user_id, image_filename=None, image_url=None):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.image_filename = image_filename
        self.image_url = image_url

    def __repr__(self):
        return "Post ID: {  } -- Date: {  } --- {  } ".format(self.id, self.date, self.title)

class Comments(db.Model, UserMixin):

    __tablename__ = 'comments'

    users = db.relationship(User)

    blogs = db.relationship(BlogPost)

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_num = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_num = db.Column(
        db.Integer, db.ForeignKey('blogposts.id'), nullable=False)
  

    def __init__(self, text, user_num, blog_num):
        self.text = text
        self.user_num = user_num
        self.blog_num = blog_num

    def __repr__(self):
        return "{self.text}"

# Admin Model and View
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.username == 'admin' 
    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('core.index', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.username == 'admin'
    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('core.index', next=request.url))


admin = Admin(app, index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(BlogPost, db.session))