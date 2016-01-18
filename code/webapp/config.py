from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from flaskext.mysql import MySQL
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
# uncomment to turn on debugging
app.config['DEBUG'] = True

app.config.update(
  # EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'email',
    MAIL_PASSWORD = 'password',
  # MySQL configurations
    MYSQL_DATABASE_USER = 'root',
    MYSQL_DATABASE_PASSWORD = 'password',
    MYSQL_DATABASE_DB = 'garbageday',
    MYSQL_DATABASE_HOST = 'localhost',
  # Secret Passwords!
    SECRET_KEY = 'password1',
    SECURITY_PASSWORD_SALT = 'password2'
    )

mail = Mail(app)
mysql = MySQL()
mysql.init_app(app)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)

key = URLSafeTimedSerializer(app.config["SECRET_KEY"])
