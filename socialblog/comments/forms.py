from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField

class CommentForm(FlaskForm):
    text = TextAreaField('Comment')
    submit = SubmitField('Submit')