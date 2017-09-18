import os
import sys
import json
import requests

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from random import randint

from flask import Flask, request

app = Flask(__name__)

friends_gt = ['cosmicphantasma']#, 'DatSW33SH', 'Fly Nikes All Day', 'Spectra SIGNS', 'Two Eyed Human', 'Unsung Samurai']

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log('Recieved {}'.format(data))

	if 'roll' in data['text'].lower() and 'die' in data['text'].lower():
		roll_dice(data)
	elif 'whos online' in data['text']:
		whosOnline(data)

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
	send_message("Your die landed on " + str(result_dice))

def getUserPresence(gt):
	xboxURL = 'https://xboxapi.com/v2/'

	headers = {
    	'X-AUTH': os.getenv('XBOX_API_ID'),
	}
	
	responseBody = requests.get('https://xboxapi.com/v2/Unsung Samurai/presence', headers=headers, verify=False)

	responsePL = responseBody.json()

#	headers = {'X-Auth': os.getenv('XBOX_API_ID')}
#	result = requests.get(xboxURL + gt + '/presence', headers=headers)
	##result = request.POST.get(xboxURL + gt + '/presence', headers=headers)

##	res = self.request("https://xboxapi.com/v2/" + gt + "/presence".format(xuid))
	return responsePL

def whosOnline(data):
	retStr = ""
	for gt in friends_gt:
		gt_res = getUserPresence(gt)
		if gt_res['state'] == "Online":
			retStr = retStr + "\n" + gt
	if len(retStr) <= 1:
		send_message("Nobody is online")
	else:
		send_message(retStr)
