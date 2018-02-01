# This file contains the class to manage chat for a session(Creating a new instance and
# generating a response for a message)

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
from modules import Router
from modules import ApiAiInstanceCreator

class Chat:

   def __init__(self, sessionId):
      self.sessionId = sessionId
      self.router = Router(self.sessionId)
      apiInstantiator = ApiAiInstanceCreator()
      self.ai = apiInstantiator.instantiate()

   def getResponse(self, message):
      request = self.ai.text_request()
      request.session_id = self.sessionId
      request.query = message
      response = json.loads(request.getresponse().read())
      parsed_response = json.dumps(response, indent=4, sort_keys=True)
      print parsed_response

      #print "Expected Action - ", self.router.next_expected_action

      #print "Received Action - ",response["result"]["action"]

      #print "Is expected Action -",self.router.is_expected_action(response['result']['action'])

      if self.router.is_expected_action(response['result']['action']):
         responseMsgs = self.router.route(response)

      else:
         if 'alternateResult' in response:
            if response['alternateResult']['fulfillment']['speech']:
               if response['alternateResult']['score'] > response['result']['score']:
                  responseMsgs = response['alternateResult']['fulfillment']['speech']
               else:
                  responseMsgs = self.router.route(response)
            else:
               responseMsgs = self.router.route(response)
         else:
            if response['result']['source'] == 'domains':
               responseMsgs = response['result']['fulfillment']['speech']
            else:
               responseMsgs = self.router.route(response)
      print responseMsgs
      return responseMsgs

   def get_response_to_event(self, response):
      #print "Expected Action - ", self.router.next_expected_action
      #print "Received Action - ",response["result"]["action"]
      #print "Is expected Action -",self.router.is_expected_action(response['result']['action'])
      responseMsgs = self.router.route(response)
      return responseMsgs