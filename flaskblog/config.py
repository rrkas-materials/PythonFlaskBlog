class Config:
    SECRET_KEY = '1ee79fcbd2bb2730153928946a4ec1fb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '<MAIL ID HERE>'  # TODO: change to your email
    MAIL_PASSWORD = '<PASSWORD HERE>'  # TODO: change to your password