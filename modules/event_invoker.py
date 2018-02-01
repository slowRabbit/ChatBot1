# This file contains the class used for invoking a dialogflow event
from apiai_instance_creator import ApiAiInstanceCreator
from constants import API_AI_CLIENT_ACCESS_TOKEN

import os.path
import sys
import json

try:
	import apiai
except ImportError:
	sys.path.append(
	os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
	)
	import apiai

class EventInvoker:
	def invoke(self, eventName, sessionId, params):
		print "Calling event - ",eventName
		ai = apiai.ApiAI(API_AI_CLIENT_ACCESS_TOKEN)
		event = apiai.events.Event(eventName)
		if params:
			event._data = params

		request = ai.event_request(event)
		request.session_id = sessionId
		response = json.loads(request.getresponse().read())
		return response