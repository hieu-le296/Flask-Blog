# blog_posts/views.py

from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from socialblog import db
from socialblog.models import BlogPost, Comments
from socialblog.blog_posts.forms import BlogPostForm
from socialblog import images


blog_posts = Blueprint('blog_posts', __name__)

# CREATE
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            filename = images.save(request.files['post_image'])
            url = images.url(filename)
            blog_post = BlogPost(title=form.title.data,
                             text=form.text.data, user_id=current_user.id, image_filename=filename, image_url=url)

        else:
            blog_post = BlogPost(title=form.title.data,
                             text=form.text.data, user_id=current_user.id)
         
        db.session.add(blog_post)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


# Blog Post (VIEW)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if Comments.query.count() == 0:
        return render_template('blog_post.html',
                            title=blog_post.title,
                            date=blog_post.date,
                            post=blog_post)
    
    else:
        comment = Comments.query.filter_by(blog_num=blog_post_id).all()
        return render_template('blog_post_comments.html',
                               title=blog_post.title,
                               date=blog_post.date,
                               post=blog_post,
                               comment=comment)

# UPDATE
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            blog_post.title = form.title.data
            blog_post.text = form.text.data
            filename = images.save(request.files['post_image'])
            url = images.url(filename)
            blog_post.image_filename = filename
            blog_post.url = url
        else:
            blog_post.title = form.title.data
            blog_post.text = form.text.data

        

        db.session.commit()
        flash(u'Your Post has been updated', 'alert alert-success')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))

# Populate the data to the fields
    form.title.data = blog_post.title
    form.text.data = blog_post.text
    return render_template('create_post.html', title='Updating', form=form)


# DELETE
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash(u'Blog Post Deleted', 'alert alert-warning')
    return redirect(url_for('core.index'))
