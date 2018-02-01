import json

import requests
from flask import Flask, request, jsonify
from types import *

from chat.chat_session import ChatSession
from handlers.message import MessageHandler
from handlers.events import EventHandler
from modules import EventInvoker

from sentiment import SentimentAnalysisClass

chatSessionHandler = ChatSession()
messageHandler = MessageHandler()
eventHandler = EventHandler()
eventInvoker = EventInvoker()
Sentiment = SentimentAnalysisClass()

app = Flask(__name__)

# App route for facebook messenger to check if server is running
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "1234567890":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200



# Note - Change the above & following route to /messenger when integrating more IM's



# App route to recieve messages from facebook messenger
@app.route('/', methods=['POST'])
def messengerHook():
    # Getting data from request and sending for resolution
    data = request.get_json()
    resolvedData = messageHandler.handle(data, "facebook")
    response = getReply(resolvedData)
    print response
    handleResponse(resolvedData["senderId"],response)
    return "ok", 200


# App route to recieve messages from web browser
@app.route('/browser', methods=['GET'])
def browserHook():
    resolvedData = request.args
    response = getReply(resolvedData)
    print response
    return jsonify(response)

# Function to get reply from the server to send back to the platform
def getReply(resolvedData):
    # Getting sender Id and message from resolved messaging event
    senderId = resolvedData["senderId"]
    is_postback_event = resolvedData["isPostBackEvent"]
    #is_postback_event = False

    # Checking & retrieving an active chat session & creating if none exists
    chatSession = chatSessionHandler.getChatSession(senderId)

    # Getting a response from the session to reply to the User
    if is_postback_event:
        event_called = resolvedData["eventCalled"]
        response = eventInvoker.invoke(event_called, chatSession.sessionId, {})
        response = chatSession.get_response_to_event(response)
    else:
        messageText = resolvedData["message"]
        response = chatSession.getResponse(messageText)
        print "******* in app"
        print response
        print "******* in app"
    return response

# Function to handle response sent from the server
def handleResponse(senderId, response):
    if type(response) is list:
        for message in response:
            send_message(senderId, message)
    else:
        send_message(senderId, response)


# Function to send message to facebook messenger user
def send_message(recipient_id, message_text):
    params = {
        "access_token": "EAAEkyBZC1iZBMBAO43btZBfdy9hf9sitn0BNnXCbtRkzT0ZA84aPCrRSkZB00tFIzrijQGsGoi8oBoputQ6pZCPwlx3oMGI3QCRIDm4uApsKKVR02dtBDsZCbmlLNFNpjgb7EkeZBj0iUhE02VTgutGhdyscIdzHcxHs6yYGKKw4HAZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    response = response.content
    print response

@app.route('/getAllChats', methods = ['GET'])
def getAllChats():
    resposneGetAllChats = Sentiment.getAllChats()
    return resposneGetAllChats

@app.route('/postChat', methods =['POST'])
def postChat():
    response = request.get_json()
    chat = response.get('chat')
    time = response.get('time')
    responsePostChat = Sentiment.postChat(chat, time)
    return responsePostChat

@app.route('/resetChatList', methods =['POST'])
def resetChatList():
    resposneResetChatList = Sentiment.resetChatList()
    return resposneResetChatList



if __name__ == '__main__':
    app.run(debug=True)