import json, urllib
from flask import Flask, request, abort
import requests

def get_url(url):
    result = requests.get(url)
    return json.loads(result.content)
"""
result = get_url("http://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:WLANWRLOGD")

#print result["type"]

#print result["features"][0]["type"]
# the line above = go to list entry "features" go to the first entry in the dictionairy and print dictionary of "type"

for features in result["features"]:
    print features["properties"]["NAME"]
"""
def wifi():
    result = get_url("http://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:WLANWRLOGD")

    # Create a list which we'll use for collecting the wifi router results
    entries = []

    # Iterate through each entry in the results
    for entry in result["features"]:
        entry = create_generic_template_element(entry["properties"]["NAME"], "http://blog.wienerlinien.at/wp-content/uploads/2016/04/header_wifi.jpg", entry["properties"]["ADRESSE"])
        # Add each wifi router to the list we've created above
        entries.append(entry)

    print entries


def create_generic_template_element(title, image_url, subtitle):
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle
    }

if __name__=="__main__":
   wifi()
#"""
