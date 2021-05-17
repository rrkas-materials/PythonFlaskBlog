import os
from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flask import current_app
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post_func():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('main.home_func'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_func(post_id):
    post = Post.query.get_or_404(post_id)
    image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
    abs_path = os.path.join(current_app.root_path, 'static', 'profile_pics', post.author.image_file)
    print(abs_path, image_file)
    if not os.path.exists(abs_path):
        image_file = url_for('static', filename='profile_pics/default.jpg')
    print(abs_path, image_file)
    return render_template('post.html', title=post.title, post=post, image_file=image_file)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def post_update_func(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.post_func', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post_func(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('main.home_func'))
