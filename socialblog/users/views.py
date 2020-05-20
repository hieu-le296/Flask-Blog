# users/views.py

from sqlalchemy.orm.exc import NoResultFound
from socialblog.users.picture_handler import add_profile_pic, add_profile_cover
from socialblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm, SendingEmail, PasswordReset, DeleteUserForm, GooglePassword
from socialblog.models import User, BlogPost
from socialblog import db, mail, oauth_blueprint
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, request, flash, redirect, redirect, Blueprint
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_dance.contrib.google import make_google_blueprint, google
import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'


users = Blueprint('users', __name__)


# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        reg_email = form.email.data

        if User.query.filter_by(email=reg_email).first():
            flash('This account already existed')
            return redirect(url_for('users.register'))
        else:
            user = User(email=form.email.data,
                        username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            msg = Message('TechTalks Blog', sender='techtalks.flaskblog@gmail.com',
                          recipients=[user.email], html=render_template('welcome.html'))
            mail.send(msg)
            flash(u'Your account has been created', 'alert alert-success')
            return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(u'Invalid email or password', 'alert alert-danger')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('core.index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@users.route('/googleregister', methods=['GET', 'POST'])
def register_google():

    form = GooglePassword()

    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()["email"]
    name = email.split('@')[0]

    if form.validate_on_submit():

        reg_email = email

        if User.query.filter_by(email=reg_email).first():
            flash('This account already existed')
            return redirect(url_for('users.login'))
        else:
            user = User(email=email,
                        username=name, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            msg = Message('TechTalks Blog', sender='techtalks.flaskblog@gmail.com',
                          recipients=[user.email], html=render_template('welcome.html'))
            mail.send(msg)
            flash(u'Your account has been created', 'alert alert-success')
            return redirect(url_for('users.login'))

    return render_template('password.html', form=form, email=email, name=name)


@oauth_authorized.connect_via(oauth_blueprint)
def google_logged_in(blueprint, token):

    form = GooglePassword()

    if form.validate_on_submit():

        resp = blueprint.session.get("/oauth_blueprint")
        assert resp.ok, resp.text

        email = resp.json()["email"]
        name = email.split('@')[0]
        password = form.password.data

        query = User.query.filter_by(email=email)

        try:
            user = query.first()

        except NoResultFound:
            user = User(email=email, username=name, password=password)

        db.session.add(user)
        db.commit()

        login_user(user)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('core.index')
        return redirect(next_page)

    return render_template('password.html', form=form)


# Sending Email
def sendresetemail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='techtalks.flaskblog@gmail.com', recipients=[user.email])
    msg.body = f'''Hello {user.username}, To reset the password, please click on this link:
    {url_for('users.reset', token=token, _external=True)}'''
    mail.send(msg)


# password reset
@users.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    form = SendingEmail()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendresetemail(user)
        return render_template('resetrequestsent.html')
    return render_template('sending_email.html', form=form)

# update password
@users.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    form = PasswordReset()

    user = User.verify_reset_token(token)
    if user is None:
        flash(u'That is an invalid token. Please enter your email address again.',
              'alert alert-warning')
        return redirect(url_for('users.resetpassword'))
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(u'Password has been reseted', 'alert alert-success')
        return redirect(url_for('users.login'))

    return render_template('reset.html', form=form)


# logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

# account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.delete.data:
            user = User.query.get(current_user.id)
            db.session.delete(user)
            db.session.flush()
            db.session.commit()
            flash('Your account has been deleted', "alert alert-success")
            return redirect(url_for('core.index'))

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        if form.picture_cover.data:
            username = current_user.username
            pic_cover = add_profile_cover(form.picture_cover.data, username)
            current_user.profile_cover = pic_cover

        if form.picture.data and form.picture_cover.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            pic_cover = add_profile_cover(form.picture_cover.data, username)
            current_user.profile_image = pic
            current_user.profile_cover = pic_cover

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated. Please hit Ctrl + F5 if you do not see the updated picture.', "alert alert-success")
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for(
        'static', filename='profile_pics/' + current_user.profile_image)

    profile_cover = url_for(
        'static', filename='profile_pics/' + current_user.profile_cover)

    return render_template('account.html', profile_image=profile_image, profile_cover=profile_cover, form=form)

# user's list of Blog Post
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
