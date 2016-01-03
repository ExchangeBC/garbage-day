import json
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/getzone')
def json_blob():
    address = request.args['address']
    zoneurl = "http://maps.kamloops.ca/arcgis3/rest/services/BCDevExchange/GarbagePickup/MapServer/3/query"
    zonepayload = {"geometryType":"esriGeometryEnvelope",
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
    zr = requests.get(zoneurl, params=zonepayload)
    zoneblob = zr.text
    almostzone = json.loads(zoneblob)
    zone = almostzone["features"][0]["attributes"]["ZONE"]
    return zone
    dateurl = "http://geoprodsvr.kamloops.ca:6080/arcgis/rest/services/BCDevExchange/GarbagePickup/MapServer/2/query"
    datepayload = {"where":"ZONE = '" + zone + "'",
	"geometryType":"esriGeometryEnvelope",
	"spatialRel":"esriSpatialRelIntersects",
	"returnGeometry":"true",
	"returnIdsOnly":"false",
	"returnCountOnly":"false",
	"returnZ":"false",
	"returnM":"false",
	"returnDistinghValues":"false",
	"f":"pjson"}
    dr = requests.get(dateurl, params=datepayload)
    dateblob = dr.text
    return dateblob

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
