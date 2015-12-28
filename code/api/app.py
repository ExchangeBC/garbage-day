# Get ready to see some bollocks

import json
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/getzone')
def json_blob():
	address = request.args['address']
	govturl = "http://maps.kamloops.ca/arcgis3/rest/services/BCDevExchange/GarbagePickup/MapServer/3/query?where=ADDRESS+%3D+%27" + address.replace(' ', '+') + "%27&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&outFields=Address%2C+Zone&returnGeometry=true&returnIdsOnly=false&returnCountOnly=false&returnZ=false&returnM=false&returnDistinctValues=false&f=pjson"
	r = requests.get(govturl)
	jsonblob = r.text
	jdict = json.loads(jsonblob)
	zone = jdict["features"][0]["attributes"]["ZONE"]
	return zone

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4321, debug=False)

