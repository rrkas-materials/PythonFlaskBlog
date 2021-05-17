import os
from flask import *
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register_func():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_func'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can log in now!', 'success')
        return redirect(url_for('users.login_func'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login_func():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_func'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Log In successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.home_func'))
        else:
            flash('Log In unsuccessful! Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout_func():
    logout_user()
    return redirect(url_for('main.home_func'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account_func():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account_func'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    abs_path = os.path.join(current_app.root_path, 'static', 'profile_pics', current_user.image_file)
    if not os.path.exists(abs_path):
        image_file = url_for('static', filename='profile_pics/default.jpg')
    print(image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_post_func(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    for post in posts.items:
        image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
        abs_path = os.path.join(current_app.root_path, 'static', 'profile_pics', post.author.image_file)
        print(abs_path, image_file)
        if not os.path.exists(abs_path):
            image_file = url_for('static', filename='profile_pics/default.jpg')
        post.author_file = image_file
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request_func():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_func'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password!', 'info')
        return redirect(url_for('users.login_func'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token_func(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home_func'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or Expired token!', 'warning')
        return redirect(url_for('users.reset_request_func'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash('Password updated! You can log in now!', 'success')
        return redirect(url_for('users.login_func'))
    return render_template('reset_token.html', title='Reset Password', form=form)
