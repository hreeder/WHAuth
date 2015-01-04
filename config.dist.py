import os

SECRET_KEY = os.urandom(64)

# Set this to False in a production environment
DEBUG = True

# ====== Database ======
# Input the relevant database URI string for your application
# Almost all major DB solutions are supported
# For more information, and requirements, see here: http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
# For example - MySQL
# SQLALCHEMY_DATABASE_URI = 'mysql://user:password@host/database'
# PostgreSQL
# SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@host/database'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

# ====== Email =======
# Define how Auth will send E-Mails
# Choose from 'smtp' or 'mailgun'
# Please open an issue if you would like to see other services supported
EMAIL_METHOD = "smtp"

# Required for SMTP mail
MAIL_SERVER = "smtp.example.com"
MAIL_PORT = 465
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "username@example.com"
MAIL_PASSWORD = "password"
DEFAULT_MAIL_SENDER = "auth@example.com"

# Required for MailGun
MG_API = "key-blahblahblah"
MG_ENDPOINT = "https://api.mailgun.net/v2/samples.mailgun.org/messages"
MG_FROM = "WHAuth <auth@example.com>"