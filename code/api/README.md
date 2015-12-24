##Purpose:  
This Flask app takes an HTTP request containing an address, accesses an [API](http://geoprodsvr.kamloops.ca:6080/arcgis/rest/services/BCDevExchange/GarbagePickup/MapServer), and returns the garbage zone data for that address.

##Requirements:
The following must be installed on the machine:
- [Flask](http://flask.pocoo.org/)  
    pip install Flask
- [requests](http://docs.python-requests.org/en/latest/)
