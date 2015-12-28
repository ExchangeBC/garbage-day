import requests
from flask import Flask, request

app = Flask(__name__)

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
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

