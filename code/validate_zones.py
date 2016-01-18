# cronned right before the email blast - so we can troubleshoot missing
# addresses with the city without impacting customer experience on signup.
import json
import requests
import time
import MySQLdb
from webapp.config import app
cnx = MySQLdb.connect(passwd=app.config['MYSQL_DATABASE_PASSWORD'],
                        db=app.config['MYSQL_DATABASE_DB'],
                        host=app.config['MYSQL_DATABASE_HOST'],
                        user=app.config['MYSQL_DATABASE_USER'])
cursor = cnx.cursor()

cursor.execute("SELECT id, address FROM users WHERE confirmed=1 AND zone IS NULL")
for (rowid, address) in cursor:
    address = address.split(',')[0].upper()
    zoneurl = ("http://maps.kamloops.ca/arcgis3/rest/services/BCDevExchange" +
               "/GarbagePickup/MapServer/3/query")
    zonepayload = {"geometryType": "esriGeometryEnvelope",
                   "where": "ADDRESS='" + address + "'",
                   "spatialRel": "esriSpatialRelIntersects",
                   "outFields": "Address, Zone",
                   "returnGeometry": "true",
                   "returnIdsOnly": "false",
                   "returnCountOnly": "false",
                   "returnZ": "false",
                   "returnM": "false",
                   "returnCountOnly": "false",
                   "f": "pjson",
                   "returnDistinctValues": "false"}
    zr = requests.get(zoneurl, params=zonepayload)
    print zr.text
    zoneblob = zr.text
    almostzone = json.loads(zoneblob)
    if len(almostzone["features"]) > 0:
        zone = almostzone["features"][0]["attributes"]["ZONE"]
        cursor.execute("UPDATE users SET zone=%s WHERE id=%s", (zone, rowid))
        cnx.commit()
    else:
        print "no zone info"
cursor.close()
cnx.close()
