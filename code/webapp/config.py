from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from flaskext.mysql import MySQL
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
# uncomment to turn on debugging
app.config['DEBUG'] = True

app.config.update(
    MAIL_SERVER='x',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='x',
    MAIL_PASSWORD='x',
    MYSQL_DATABASE_USER='x',
    MYSQL_DATABASE_PASSWORD='x',
    MYSQL_DATABASE_DB='x',
    MYSQL_DATABASE_HOST='x',
    SECRET_KEY='x',
    SECURITY_PASSWORD_SALT='x'
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
