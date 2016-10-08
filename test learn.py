import json, urllib
from flask import Flask, request, abort
import requests


# this works

def get_url(url):
    result = requests.get(url)
    return json.loads(result.content)

#json_file_from_the_website = get_url("http://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:WLANWRLOGD")

#print result["type"]

#print result["features"][0]["type"]
# the line above = go to list entry "features" go to the first entry in the dictionairy and print dictionary of "type"

#for things_in_that_json_file_from_the_website in json_file_from_the_website["features"]:
    #print things_in_that_json_file_from_the_website["properties"]["NAME"]


json_file_from_the_website = get_url("http://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:WLANWRLOGD")

# Create a list which we'll use for collecting the wifi router results
entries = []

def create_generic_template_element(title, image_url, subtitle):
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle
    }

# Iterate through each entry in the results
######for entry in result["features"]:
    #######entry = create_generic_template_element(feature["properties"]["NAME"], "http://blog.wienerlinien.at/wp-content/uploads/2016/04/header_wifi.jpg", entry["properties"]["ADRESSE"])


for things_in_that_json_file_from_the_website in json_file_from_the_website["features"]:
    print things_in_that_json_file_from_the_website["properties"]["NAME"]
    # Add each wifi router to the list we've created above
    entries.append(things_in_that_json_file_from_the_website)

# Add each wifi router to the list we've created above
#reply_with_generic_template(sender_id, entries)



print entries
