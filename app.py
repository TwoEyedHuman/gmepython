import os
import sys
import json
import requests

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from random import randint

from flask import Flask, request

app = Flask(__name__)

commonWords = ['a','about','all','also','and','as','at','be','because','but','by','can','come','could','day','do','even','find','first','for','from','get','give','go','have','he','her','here','him','his','how','I','if','in','into','it','its','just','know','like','look','make','man','many','me','more','my','new','no','not','now','of','on','one','only','or','other','our','out','people','say','see','she','so','some','take','tell','than','that','the','their','them','then','there','these','they','thing','think','this','those','time','to','two','up','use','very','want','way','we','well','what','when','which','who','will','with','would','year','you','your']

friendsGamertags = ['cosmicphantasma', 'DatSW33SH', 'FlyNikesAllDay', 'Spectra SIGNS', 'Two Eyed Human', 'Unsung Samurai']

botName = "Deckard Cain"

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log('Recieved {}'.format(data))

	if ('roll' in data['text'].lower() and 'die' in data['text'].lower()) or ('roll D' in data['text'].lower()):
		roll_dice(data)
	elif 'who' in data['text'].lower and 'online' in data['text'].lower():
		whosOnline(data)
	elif ('@dc' in data['text'].lower() or '@deckard cain' in data['text'].lower()) and ('what is ' in data['text'].lower() or 'define' in data['text'] or 'definition' in data['text']):
		definitionUD(data)

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
	numbers = [int(s.replace("D", "")) for s in data['text'].split() if s.replace("D", "").isdigit()]
	result_dice = randint(1,numbers[0])
	send_message("Your die landed on " + str(result_dice))

def whosOnline(data):
	xboxURL = 'https://xboxapi.com/v2/'
	headers = {
    	'X-AUTH': os.getenv('XBOX_API_ID'),
	}
	returnString = ""
	try:
		for gt in friendsGamertags:
			responseBody = requests.get('https://xboxapi.com/v2/' + gt + '/presence', headers=headers, verify=False)
			if responseBody.json['state'] == "Online":
				responseSystem = responseBody.json['devices'][0]['type']
				specificGamer = gt + ' is online.\n'
				for titles in responseBody.json['devices'][0]['titles']:
					if titles['placement'] == "Full" and titles['name'] != "Home":
						specificGamer = gt + ' is playing ' + titles['name'] + '\n'
				returnString = returnString + specificGamer
		if len(returnString) <= 1:
			returnString = "Nobody is online."
		send_message(returnString)
	except KeyError:
		send_message("The Keys of Hate, Terror, and Destruction are required to create the Infernal Machine.")
	except:
		send_message("Deckard Cain has been killed by butterflies.")
		
def definitionUD(data):
	udURL = 'http://api.urbandictionary.com/v0/'
	if len([x for x in data['text'] if x not in commonWords]) >= 1:
		lookupWord = [x for x in data['text'].split() if x not in set().union(commonWords,['what','is','definition','define','@','Deckard','@Deckard','Cain','deckard','cain','dc','DC','@dc','@DC'],botName.split())][0]
		try:
			responseBody = requests.get(udURL + 'define?term=' + lookupWord)
			wordDefinition = responseBody.json['list'][0]['definition']
		except:
			wordDefinition = "I cannot identify that."
		send_message(wordDefinition)
	else:
		send_message("Zod Amn Ith...how do you not know what that means?")
