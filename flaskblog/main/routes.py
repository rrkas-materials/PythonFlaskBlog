import os
from flask import render_template, request, Blueprint, url_for, current_app
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home_func():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    for post in posts.items:
        image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
        abs_path = os.path.join(current_app.root_path, 'static', 'profile_pics', post.author.image_file)
        if not os.path.exists(abs_path):
            image_file = url_for('static', filename='profile_pics/default.jpg')
        post.author_file = image_file
    return render_template('home.html', posts=posts)


@main.route('/about')
def about_func():
    return render_template('about.html', title='About')
