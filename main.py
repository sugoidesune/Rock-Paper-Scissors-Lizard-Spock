# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests, pprint

app = Flask(__name__)

access_token = 'EAAZALe3ScA2UBAKjOy5jFxJlmeYrj6ZCGU0Mvm2Q4xMbWSNN7hOZAqZByC6ZBIocowPaBwcMRsxI7e1HqkkNtayg7VtAmUdsvZARhW5sY0bry6pZATWEui4ZBSHVXpmaqGN6cotZC0TZCVhZAXuo6WE8N03J1YSy4COEkdPaMJu6PajtgZDZD'


@app.route("/", methods=["GET"])
def root():
    return "Hello World!"


# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET'])
def get_webhook():

    if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args:
        abort(400)

    return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = request.json
    print data
    if data["object"] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                if "message" in messaging_event:

                    sender_id = messaging_event['sender']['id']

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text']
                        if isitgreeting(message_text):
                            reply_with_text(sender_id, "Hi there. Let's Play Rock Paper Scissors Lizard Spock!")
                        elif isitgoodbye(message_text):
                            reply_with_text(sender_id, "Oh... Sorry to see you go, see ya!")
                        elif message_text == "json":
                            reply_with_text(sender_id, "Heres the json file forya")
                            reply_with_text(sender_id, data)
                elif "postback" in messaging_event:
                    print("postback was recognized")
                    received_postback(messaging_event);
                    return "ok", 200

    return "ok", 200


"""
def blabla():
	while True:
		text=str(raw_input("type abc please"))
		if isitgreeting(text):
			print "hell yeah thats a greeting"


def isitgreeting(text):
	mylist = ("hi", "hallo", "hello", "yo", "sup", "whats up", "what/'s up", "whazza",)
	for all_the_entries in mylist:
		#print s
		if text.lower() in all_the_entries.lower():
			return True
			#print all_the_entries
blabla()
"""
def isitgreeting(text):
	mylist = ("hi", "hallo", "hello", "yo", "sup", "whats up", "what/'s up", "whazza", "whatsup", "lets go", "start")
	for all_the_entries in mylist:
		if text.lower() in all_the_entries.lower():
			return True

def isitgoodbye(text):
	mylist = ("Stop", "Unsubscribe", "Cancel", "Fuck off", "Fuck you", "Goodbye", "bye", "STFU", "go away", "no more", "no")
	for all_the_entries in mylist:
		if text.lower() in all_the_entries.lower():
			return True

def received_postback(event):
    global index
    sender_id = event['sender']['id']
    payload = event['postback']['payload']
    pp.pprint(payload)
    print("received_postback achieved")
    """
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
    """
    if 'GREETINGS_MY_FRIEND' in payload:
        pp.pprint('GREETINGS_MY_FRIEND')
        reply_with_text(sender_id, "Let's Play Rock Paper Scissors Lizard Spock!")

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
