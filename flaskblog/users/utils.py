import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from flaskblog import  mail, users
from flaskblog.models import User


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_name)
    out_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(out_size)  # resize image
    i.save(picture_path)
    print(current_app.root_path)
    if current_user.image_file != 'default.jpg' and os.path.exists(
            os.path.join(app.root_path, 'static', 'profile_pics', current_user.image_file)):
        os.remove(os.path.join(app.root_path, 'static', 'profile_pics', current_user.image_file))
    return picture_name


def send_reset_email(user: User):
    token = user.get_reset_token()
    msg = Message(
        'Password Reset',
        sender='RRKAS@FlaskBlogApp',
        recipients=[user.email],
    )
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token_func', token=token, _external=True)}

Link expires within 30 minutes!

If you did not make this request, ignore this mail.

Team RRKAS@FlaskBlog
    '''
    mail.send(msg)
