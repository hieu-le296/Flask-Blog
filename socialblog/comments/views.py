from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from socialblog import db
from socialblog.models import Comments, BlogPost
from socialblog.comments.forms import CommentForm

user_comments = Blueprint('user_comments', __name__)


# CREATE
@user_comments.route('/createcomment/<int:blog_post_id>', methods=['GET', 'POST'])
@login_required
def create_comment(blog_post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment_post = Comments(text=form.text.data,
                                user_num=current_user.id,
                                blog_num=blog_post_id)

        db.session.add(comment_post)
        db.session.commit()
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))

    return render_template('create_comment.html', form=form)

# Comments (VIEW)
@user_comments.route('/<int:blog_post_id>')
def comments_user(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    comment_post = Comments.query.all()
    return render_template('blog_post.html',
                            title=blog_post.title,
                            date=blog_post.date,
                            post=blog_post)


# Edit Comment
@user_comments.route('/update_comment/<int:comments_post_id>', methods=['GET', 'POST'])
@login_required
def update_comment(comments_post_id):
    comment_post = Comments.query.get(comments_post_id)
    blog_post_id = comment_post.blog_num

    form = CommentForm()

    if form.validate_on_submit():
        comment_post.text = form.text.data
        db.session.commit()
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))

    # Populate the data to the field
    form.text.data = comment_post.text
    return render_template('create_comment.html', form=form)


# Delete Comment
@user_comments.route('/delete/<int:comments_post_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comments_post_id):
    comment = Comments.query.get_or_404(comments_post_id)
    blog_post_id = comment.blog_num

    if comment.author != current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))

