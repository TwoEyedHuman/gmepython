import os
import sys
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from random import randint

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log('Recieved {}'.format(data))

	if 'roll' in data['text'] and die in data['text']:
		roll_dice(data)

	return "ok", 200

def send_message(msg):
	url	= 'https://api.groupme.com/v3/bots/post'

	data = {
					'bot_id' : os.getenv('GROUP_ME_BOT_ID'),
					'text'	 : msg,
				 }
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
	
def log(msg):
	print(str(msg))
	sys.stdout.flush()

def roll_dice(data):
	numbers = [int(s) for s in data['text'].split() if s.isdigit()]
	result_dice = randint(1,numbers[0])
	send_message("Your die landed on " + result_dice)
