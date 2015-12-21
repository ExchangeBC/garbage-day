from flask import Flask, render_template, request, json, redirect
from flask_mail import Message, Mail
from flask.ext.mysql import MySQL

app = Flask(__name__)
#app.config['DEBUG'] = True

ADMINS = ['email']
app.config.update(
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = ADMINS[0],
        MAIL_PASSWORD = 'password'
        )

mail = Mail(app)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'garbageday'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    try:
	# read the posted values from the UI
	_address = request.form['inputAddress']
	_email = request.form['inputEmail']
        # validate the received values
        if _address and _email:	
	    conn = mysql.connect()
	    cursor = conn.cursor()
	    cursor.callproc('sp_createUser',(_email,_address))
	    data = cursor.fetchall()
	    if len(data) is 0:
		msg = Message("Garbage Alert Signup", sender=ADMINS[0], recipients=[_email])
        	msg.html = '<b>Email Confirmation Test Complete</b>'
        	mail.send(msg)
		conn.commit()
	        return render_template('confirmation.html')
	    elif str(data[0]) == "(u'Email has already been used!',)":
                return render_template("alreadyused.html")
	    else:
		return json.dumps({'error1':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error2':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
