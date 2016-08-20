# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
from random import randint
import requests

app = Flask(__name__)

access_token = 'EAAZALe3ScA2UBAKjOy5jFxJlmeYrj6ZCGU0Mvm2Q4xMbWSNN7hOZAqZByC6ZBIocowPaBwcMRsxI7e1HqkkNtayg7VtAmUdsvZARhW5sY0bry6pZATWEui4ZBSHVXpmaqGN6cotZC0TZCVhZAXuo6WE8N03J1YSy4COEkdPaMJu6PajtgZDZD'


@app.route("/", methods=["GET"])
def root():
    return "Hello World! + Token"


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
                        #image = "http://cdn.shopify.com/s/files/1/0080/8372/products/tattly_jen_mussari_hello_script_web_design_01_grande.jpg"
                        #element = create_generic_template_element("Hello", image, message_text)
                        #reply_with_generic_template(sender_id, [element])
                        game()

                        do_rules(sender_id, message_text)

    return "ok", 200


#####################################Rock paper scissors#############################################
chand = ""
rnumber =randint(0,8)

def define():
	global chand
	global rnumber
	rnumber =randint(0,8)
	if rnumber <3:
		chand = "Rock"
	elif rnumber >2 and rnumber <6:
		chand = "Scissors"
	else:
		chand = "Paper"

def game():
	while True:
		define()
		reply_with_text(recipient_id, "Which hand do you want to play- Rock, Paper, Scissors, Lizard, Spock")
		input = raw_input()
		if input == chand:
			reply_with_text(recipient_id,  "You both had %s" % (input))
		elif input != "Scissors" and input != "Paper" and input != "Rock":
			reply_with_text(recipient_id,  "How you gonna beat %s with \"%s\"" % (chand, input))
			reply_with_text(recipient_id,  "Try again:")
		else:
			if chand == "Scissors" and input == "Rock":
				reply_with_text(recipient_id,  "Rock crushes Scissors!")
				reply_with_text(recipient_id,  "You win")
			elif chand == "Scissors" and input == "Paper":
				reply_with_text(recipient_id,  "Scissors cut Paper!")
				reply_with_text(recipient_id,  "You lost")
			elif chand == "Rock" and input == "Paper":
				reply_with_text(recipient_id,  "Paper covers Rock!")
				reply_with_text(recipient_id,  "you win")
			elif chand == "Rock" and input == "Scissors":
				reply_with_text(recipient_id,  "Rock crushes Scissors!")
				reply_with_text(recipient_id,  "you lose")
			elif chand == "Paper" and input == "Scissors":
				reply_with_text(recipient_id,  "Scissors cut Paper!")
				reply_with_text(recipient_id,  "You lose")
			elif chand == "Paper" and input == "Rock":
				reply_with_text(recipient_id,  "Paper covers Rock!")
				reply_with_text(recipient_id,  "You lose")
			else:
				reply_with_text(recipient_id,  "Dont try to cheat please")

game()
#####################################Rock paper scissors#############################################
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
