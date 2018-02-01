#this class would bring the sentiment from google cloud and return a object containing 
#score and magnitude

import json
import urllib2
import Chat as c1

baseURL = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key='
apiKey  = 'AIzaSyALKmvtumwuY16LUpop5Q5M4SQy6z1Q5l4'

def getSentimentAnalyzedChat(chat, time):        
    
    data = {
              'document': {
                  'type': 'PLAIN_TEXT',
                  'content': chat,
              }
          }
    
    req = urllib2.Request(baseURL+apiKey)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    response = response.read()
    jsonResponse = json.loads(response)
    
    print (response)
    
    documentSentiment  = jsonResponse['documentSentiment']
    score = documentSentiment.get('score')
    magnitude = documentSentiment.get('magnitude')
    factor = score * magnitude
    factor = str(round(factor, 2))
    
    print ('score is : ', score)
    print ('magnitude is : ', magnitude)# -*- coding: utf-8 -*-
    print ('overall factor is :', factor)
    
    Chat1 = c1.Chat(chat, time, score, magnitude, factor)
    return Chat1


#getSentimentAnalyzedChat('10:45', 'thank you for your good service')
#getSentimentAnalyzedChat('10:45', 'very bad service, i am just frustated')