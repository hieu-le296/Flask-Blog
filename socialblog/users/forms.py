from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from socialblog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    ResetPasswordButton = SubmitField('Reset Password')
    remember_me = BooleanField('Remember Password')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_confirm', message='Password Must Match')])
    password_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('You email has been registered already')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValueError('You username has been registered already')


class SendingEmail(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('You email has been registered already')


class PasswordReset(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_confirm', message='Password Must Match')])
    password_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    picture_cover = FileField('Update Profile Cover', validators=[
                                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Account')
    delete = SubmitField('Delete')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('You email has been registered already')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValueError('You username has been registered already')


class DeleteUserForm(FlaskForm):
    delete = SubmitField('Delete')

class GooglePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register!')