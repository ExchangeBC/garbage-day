#once a year really
from webapp.config import app
import json
import requests
import time
import MySQLdb
cnx = MySQLdb.connect(passwd=app.config['MYSQL_DATABASE_PASSWORD'],
                        db=app.config['MYSQL_DATABASE_DB'],
                        host=app.config['MYSQL_DATABASE_HOST'],
                        user=app.config['MYSQL_DATABASE_USER'])
cursor = cnx.cursor()

for zone in range(1, 6):
    dateurl = ("http://geoprodsvr.kamloops.ca:6080/arcgis/rest/" +
               "services/BCDevExchange/GarbagePickup/MapServer/2/query")
    datepayload = {"where": "ZONE = '" + str(zone) + "'",
                   "geometryType": "esriGeometryEnvelope",
                   "spatialRel": "esriSpatialRelIntersects",
                   "returnGeometry": "true",
                   "returnIdsOnly": "false",
                   "returnCountOnly": "false",
                   "returnZ": "false",
                   "returnM": "false",
                   "returnDistinghValues": "false",
                   "f": "pjson"}
    dr = requests.get(dateurl, params=datepayload)
    dateblob = json.loads(dr.text)
    for datejson in dateblob['features']:
        thedate = int(datejson["attributes"]["PICKUPDATE"]) / 1000
        cursor.execute("insert into zones (zone, pickupdate) values (%s, %s)", (zone, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(thedate))))
        print str(zone) + " - " + time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(thedate))

cnx.commit()
cursor.close()
cnx.close()
