from flask import render_template, request, json, redirect, url_for
from config import app, mysql, send_email, key
import requests
import json

# home page
@app.route("/")
def main():
    return render_template('index.html')

# sign-up page
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# does the dirty work for signing users up
@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        # read the posted values from the UI
        address = request.form['inputAddress']
        email = request.form['inputEmail']
        # validate the received values
        if address and email:	
            conn = mysql.connect()
            cursor = conn.cursor()
            # adds user to db	    
            if cursor.execute('select (1) from users where email = %s limit 1', (email)):
                return render_template("alreadyused.html")
            else:
                # creates user
                cursor.execute('insert into users (email,zone) values (%s,%s)', (email,address))
                # sends confirmation email
                token = key.dumps(email, salt='email-confirm-key')
                confirm_url = url_for('confirm_email',token=token,_external=True)
                subject = "Confirm Your Email"
                html = render_template('emailconfirm.html',confirm_url=confirm_url)
                send_email(email, subject, html)
                conn.commit()
                return render_template('confirmation.html')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error2':str(e)})
    finally:
        cursor.close() 
        conn.close()

# confirms the user's email when they click the unique link
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = key.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        return "error"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT confirmed FROM users WHERE email=%s', (email))
    data = cursor.fetchall()
    # checks if user is already confirmed
    if str(data[0][0]) == "1":
        return render_template("alreadyconfirmed.html")
    else:
	# updates confirmed column to '1'
        cursor.execute("UPDATE users SET confirmed='1' WHERE email=%s", (email))
        conn.commit()
        return render_template("activated.html")
    cursor.close()
    conn.close()

@app.route('/getzone')
def json_blob():
    address = request.args['address']
    govturl = "http://maps.kamloops.ca/arcgis3/rest/services/BCDevExchange/GarbagePickup/MapServer/3/query"
    payload = {"geometryType":"esriGeometryEnvelope",
        "where":"ADDRESS = '" + address + "'",
        "spatialRel":"esriSpatialRelIntersects",
        "outFields":"Address, Zone",
        "returnGeometry":"true",
        "returnIdsOnly":"false",
        "returnCountOnly":"false",
        "returnZ":"false",
        "returnM":"false",
        "returnCountOnly":"false",
        "f":"pjson",
        "returnDistinctValues":"false"}
    r = requests.get(govturl, params=payload)
    jsonblob = r.text
    jdict = json.loads(jsonblob)
    zone = jdict["features"][0]["attributes"]["ZONE"]
    return zone

if __name__ == "__main__":
    app.run(host="0.0.0.0")
