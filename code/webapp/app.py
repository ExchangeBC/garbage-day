from config import app
from config import key
from config import mysql
from config import send_email
from flask import json
from flask import render_template
from flask import request
from flask import url_for

# app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signUp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        # read the posted values from the UI
        address = request.form['inputAddress']
        email = request.form['inputEmail']
        # validate the received values
        if address and email:
            if "'" in email or '"' in email or "(" in email or " )" in email:
                raise Exception
            if ',' in email or ";" in email or "%" in email:
                raise Exception
            if '"' in address or "(" in address or " )" in address:
                raise Exception
            if "'" in address or ";" in address or "%" in address:
                raise Exception
            query = "SELECT * FROM users WHERE email=%s AND address=%s"
            cursor.execute(query, (email, address))
            data = cursor.fetchall()
            if len(data) is 0:
                query = "INSERT INTO users (email, address) values (%s,%s)"
                cursor.execute(query, (email, address))
                conn.commit()
                cursor.close()
                conn.close()
            if cursor.execute('select (1) from users where email = %s limit 1',
                              (email)):
                return render_template("alreadyused.html")
            else:
                # creates user
                cursor.execute('insert into users (email,zone) values (%s,%s)',
                               (email, address))
                # sends confirmation email
                token = key.dumps(email, salt='email-confirm-key')
                confirm_url = url_for('confirm_email',
                                      token=token, _external=True)
                subject = "Confirm Your Email"
                html = render_template('emailconfirm.html',
                                       confirm_url=confirm_url)
                send_email(email, subject, html)
                return render_template('confirmation.html')
        else:
            cursor.close()
            conn.close()
            return json.dumps({'html':
                               '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error2': str(e)})


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = key.loads(token, salt="email-confirm-key", max_age=86400)
        if "'" in email or '"' in email or "(" in email or " )" in email:
            raise Exception
        if ',' in email or ";" in email or "%" in email:
            raise Exception
    except Exception as e:
        return str(e)
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT confirmed FROM users WHERE email=%s', (email,))
        data = cursor.fetchall()
    except Exception as e:
        return str(e)
    if str(data[0][0]) == "1":
        return render_template("alreadyconfirmed.html")
    else:
        try:
            cursor.execute("UPDATE users SET confirmed='1' WHERE email=%s",
                           (email,))
            conn.commit()
            return render_template("activated.html")
        except Exception as e:
            return str(e)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8085")
