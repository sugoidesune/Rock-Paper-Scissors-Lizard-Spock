import json, urllib
from flask import Flask, request, abort
import requests

def get_url(url):
    result = requests.get(url)
    return json.loads(result.content)

result = get_url("http://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:WLANWRLOGD")

#print result["type"]

#print result["features"][0]["type"]
# the line above = go to list entry "features" go to the first entry in the dictionairy and print dictionary of "type"

for features in result["features"]:
    print features["properties"]["NAME"]
