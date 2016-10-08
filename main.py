# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests
import dateparser
import re



app = Flask(__name__)

access_token = 'EAAYPCWbw5mYBAIawH5B4azSURXsG1XwMqZCqtKDCVQfD3zZB0pdmBIxJH8rjPbxYl06NSGWudgKS0TxmzU5foyLjZABPtQy5E2AB5thv6vqMJ56RrcDjGZBVJi7DIGd1vh4Q3T8x54nBj2cttTuTlGOZCNrisqZB61Cy2xw97ZAtwZDZD'

result=""

@app.route("/", methods=["GET"])
def root():
    return "Hello World!"

#blub
# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET'])
def get_webhook():

    if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args:
        abort(400)

    return request.args.get('hub.challenge')



@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = request.json
    if data["object"] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                if "message" in messaging_event:

                    sender_id = messaging_event['sender']['id']

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text']
                        date= str(dateparser.parse(message_text))
                        reply_with_text(sender_id, "http://tv.orf.at/program/orf1/"+re.sub("-","",date[:10]))





                        # basic level
                        ##if message_text == "Time":
                            ##print "in wifi"
                            # Fetch the data from Wiener Linien's API

                            #result = get_url("http://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:WLANWRLOGD")

                            # Create a list which we'll use for collecting the wifi router results
                            #entries = []

                            # Iterate through each entry in the results
                            #for entry in result["broadcasts"]:
                                #print "in broadcasts"
                                #entry = create_generic_template_element(entry["title"], "http://tvthek.orf.at/static/images/logo_orf_header.png", entry["subTitle"])
                                # Add each wifi router to the list we've created above
                                #entries.append(entry)

                            # Add each wifi router to the list we've created above
                            #reply_with_generic_template(sender_id, entries)
                            #reply_with_text(sender_id, "hi how are you doing?")
                            # After we've sent the message with the generic template we stop the code
                        #elif message_text == "hi":

                        return "ok", 200

                        #else:
                            #message_text = messaging_event['message']['text']
                            #image = "http://cdn.shopify.com/s/files/1/0080/8372/products/tattly_jen_mussari_hello_script_web_design_01_grande.jpg"
                            #element = create_generic_template_element("Hello", image, message_text)
                            #reply_with_generic_template(sender_id, [element])


                        #do_rules(sender_id, message_text)

    return "ok", 200
"""
if "message" in messaging_event:
    sender_id = messaging_event['sender']['id']
    if 'text' in messaging_event['message']:
        message_text = messaging_event['message']['text']
        if message_text == "wifi":
            # Fetch the data from Wiener Linien's API
            result = get_url("http://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&srsName=EPSG:4326&outputFormat=json&typeName=ogdwien:WLANWRLOGD")
            # Create a list which we'll use for collecting the wifi router results
            entries = []
            # Iterate through each entry in the results
            for entry in result["features"]:
                entry = create_generic_template_element(feature["properties"]["NAME"], "http://blog.wienerlinien.at/wp-content/uploads/2016/04/header_wifi.jpg", entry["properties"]["ADRESSE"])
                # Add each wifi router to the list we've created above
                entries.append(entry)
            # Add each wifi router to the list we've created above
            reply_with_generic_template(sender_id, entries)
            # After we've sent the message with the generic template we stop the code
            return "ok", 200
"""

# helper functions

def get_url(url):
    result = requests.get(url)
    return json.loads(result.content)


def do_rules(recipient_id, message_text):
    rules = {
        "Hello": "World",
        "Foo": "Bar"
    }

    if message_text in rules:
        reply_with_text(recipient_id, rules[message_text])

    else:
        reply_with_text(recipient_id, "You have to write something I understand ;)")


# reply methods

def reply_with_text(recipient_id, message_text):
    message = {
        "text": message_text
    }
    reply_to_facebook(recipient_id, message)


def reply_with_generic_template(recipient_id, elements):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
    reply_to_facebook(recipient_id, message)


def reply_with_image(recipient_id, image_url):
    message = {
        "attachment": {
            "type": "image",
            "payload": {
                "template_type": "image",
                "url": image_url
            }
        }
    }
    reply_to_facebook(recipient_id, message)


# function to send a message to facebook

def reply_to_facebook(recipient_id, message):
    params = {
        "access_token": access_token
    }

    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message
    })

    print data

    url = "https://graph.facebook.com/v2.6/me/messages?" + urllib.urlencode(params)
    r = requests.post(url=url, headers=headers, data=data)


# create template elements for carousel, images with buttons, quick replies, …

def create_generic_template_element(title, image_url, subtitle):
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle
    }


if __name__ == '__main__':
    app.run(debug=True)
