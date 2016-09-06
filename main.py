# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests

app = Flask(__name__)

access_token = 'EAAZALe3ScA2UBAKjOy5jFxJlmeYrj6ZCGU0Mvm2Q4xMbWSNN7hOZAqZByC6ZBIocowPaBwcMRsxI7e1HqkkNtayg7VtAmUdsvZARhW5sY0bry6pZATWEui4ZBSHVXpmaqGN6cotZC0TZCVhZAXuo6WE8N03J1YSy4COEkdPaMJu6PajtgZDZD'


pp = pprint.PrettyPrinter(indent=2)
index = 0

QUOTES = [
    {
        "id": "1",
        "quote": "Hass darf niemals das letzte Wort sein!",
        "answers": [
            "Alexander Van der Bellen", "Norbert Hofer"
        ],
        "correct_answer": "Alexander Van der Bellen",
        "source": "Alexander Van der Bellen in Tiroler Zeitung",
        "image_url": "https://www.vanderbellen.at/fileadmin/_processed_/csm_gemeinsam_b4bf6e7143.png"
    },
    {
        "id": "2",
        "quote": "Sie werden sich noch wundern, was alles möglich ist.",
        "answers": [
            "Alexander Van der Bellen", "Norbert Hofer"
        ],
        "correct_answer": "Norbert Hofer",
        "source": "Norbert Hofer, Elefantenrunde, ORF, 21.4.2016",
        "image_url": "https://media.giphy.com/media/ikXcqqlSNH2Mw/giphy.gif"
    },
    {
        "id": "3",
        "quote": "Die EU wird auf ein Kerneuropa reduziert werden müssen.",
        "answers": [
            "Alexander Van der Bellen", "Norbert Hofer"
        ],
        "correct_answer": "Norbert Hofer",
        "source": "Norbert Hofer in „Österreich“ am 31.1.2016",
        "image_url": "https://media.giphy.com/media/ikXcqqlSNH2Mw/giphy.gif"
    }
]

@app.route("/", methods=["GET"]) # / access root
def root():
    return "Hello Van der Bellen!" #website acces "previously hello world" compare to hello world bot from github username moocadroid


# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET']) #app.route might be from flask - prettty sure about it - everything else wouldnt make sense
def get_webhook():

    if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args: #facebook authentication if webhook works or smth
        abort(400)

    return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def post_webhook():
    global index
    data = request.json
    pp.pprint(data)
    if data["object"] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                if "message" in messaging_event:

                    sender_id = messaging_event['sender']['id']

                    if 'text' in messaging_event['message']:
                        print("text was recognized")
                        message_text = messaging_event['message']['text']
                        image = "http://cdn.shopify.com/s/files/1/0080/8372/products/tattly_jen_mussari_hello_script_web_design_01_grande.jpg"
                        element = create_generic_template_element("Hello", image, message_text)
                        #reply_with_generic_template(sender_id, [element])
                        print "Das ist mien Index %s" %index
                        send_quote(sender_id, QUOTES[index])
                        if(index < len(QUOTES)-1):
                            index += 1 # == index = index + 1
                        else:
                            index = 0
                elif "postback" in messaging_event:
                    print("postback was recognized")
                    received_postback(messaging_event);
    return "ok", 200


def send_quote(recipient_id, quote):
    buttons = []
    for answer in quote['answers']:
        buttons.append({
            "type": "postback",
            "title": answer,
            "payload": "ANSWER_%s_%s" % (quote['id'], answer)
        })

    message = {
        "attachment":{
            "type":"template",
            "payload": {
                "template_type":"button",
                "text": quote['quote'],
                "buttons": buttons
            }
        }
    }
    reply_to_facebook(recipient_id, message)

def pick_quote(Topic=None):
    return QUOTES[randint(0, len(QUOTES) - 1)] #change to pseudo random

def received_postback(event):
    global index
    sender_id = event['sender']['id']
    payload = event['postback']['payload']
    pp.pprint(payload)
    print("received_postback achieved")
    if 'ANSWER_' in payload:
        pp.pprint('ANSWER_')
        process_answer(sender_id, payload[payload.find('_') + 1:])
    elif 'NEXT_QUOTE' in payload:
        pp.pprint('NEXT_QUOTE')
        send_quote(sender_id, QUOTES[index])
        if(index < len(QUOTES)-1):
            index += 1 # == index = index + 1
        else:
            index = 0
    elif 'GETTING_STARTED' in payload:
        pp.pprint('GETTING_STARTED')
        reply_with_text_and_button(sender_id, "Willkommen bei Facts & Fiction zur Bundespräsidentenwahl 2016 - Runde 2 :) Mal sehen, wie viele Zitate du richtig erkennst!", "Zitat schicken", "NEXT_QUOTE")
        #send_quote(sender_id, pick_quote())
        # suggest_topics(sender_id)
        # send_introduction

def process_answer(sender_id, data):
    answer = data[data.find('_') + 1:]
    quote_id = data[:data.find('_')]
    for index, quote in enumerate(QUOTES):
        if quote["id"] == quote_id:
            quote = QUOTES[index]
            break

    if answer == quote['correct_answer']:
        send_success_message(sender_id, quote)
    else:
        send_fail_message(sender_id, quote)

def send_success_message(recipient_id, quote):
    message_text = "Richtig: %s hat es gesagt." % quote['correct_answer']
    #message = create_generic_template_element("Richtig!", quote['image_url'], message_text)
    reply_with_text(recipient_id, message_text)
    send_corrected_quote(recipient_id, quote)


def send_fail_message(recipient_id, quote):
    message_text = "Sorry! %s hat es gesagt." % quote['correct_answer']
    #message = create_generic_template_element("Falsch!", quote['image_url'], message_text)
    #reply_with_generic_template(recipient_id, [message])
    reply_with_text(recipient_id, message_text)
    send_corrected_quote(recipient_id, quote)

def send_corrected_quote(recipient_id, quote):
    message_text = "'" + quote['quote'] + "' (Quelle: " + quote['source'] + ")"
    message = create_generic_template_element(quote['correct_answer'], quote['image_url'], message_text)
    reply_with_generic_template(recipient_id, [message])
    reply_with_button(recipient_id, "Nächstes Zitat", "NEXT_QUOTE")


def reply_for_next_quote(recipient_id, message_text):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": message_text,
                "buttons": [{
                    "type": "postback",
                    "title": "Nächstes Zitat",
                    "payload": "NEXT_QUOTE"
                }]
            }
        }
    }
    reply_to_facebook(recipient_id, message)

def reply_with_text_and_button(recipient_id, message_text, button_text, button_payload):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": message_text,
                "buttons": [{
                    "type": "postback",
                    "title": button_text,
                    "payload": button_payload
                }]
            }
        }
    }
    reply_to_facebook(recipient_id, message)

def get_url(url):
    result = request.get(url)
    return json.loads(result.content)


def reply_with_text(recipient_id, message_text):
    message = {
        "text": message_text
    }
    reply_to_facebook(recipient_id, message)

def reply_with_button(recipient_id, button_text, button_payload):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Möchtest du weiterspielen?",
                "buttons": [{
                    "type": "postback",
                    "title": button_text,
                    "payload": button_payload
                }]
            }
        }
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


def create_generic_template_element(title, image_url, subtitle):
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle
    }

if __name__ == '__main__':
    app.run(debug=True)
