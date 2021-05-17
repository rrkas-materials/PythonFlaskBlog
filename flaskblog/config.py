class Config:
    SECRET_KEY = '1ee79fcbd2bb2730153928946a4ec1fb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'flaskblog.rrkas@gmail.com'  # TODO: change to your email
    MAIL_PASSWORD = 'BLOGrrkasFLASK!'  # TODO: change to your password