# This file contains the class to retrieve & return data from facebook message event

class FacebookHandler:

	# Function to get data from fb messaging event
	def getData(self, data):
		# Iterating through response to retrieve message sent by user
		if data["object"] == "page":
			for entry in data["entry"]:
				for messaging_event in entry["messaging"]:
					if messaging_event.get("message"):
						is_echo = False

						# Checking if recieved message is an echo event or not
						if "is_echo" in messaging_event["message"]:
							is_echo = True

						# Acting if received message is not an echo event
						if(is_echo):
							pass
						else:
							# Retrieving sender Id and message from messaging event
							senderId = messaging_event["sender"]["id"]
							if 'text' in messaging_event["message"]:
								messageText = messaging_event["message"]["text"]
							else:
								messageText = "Good Day!!!"

							resolvedData = {
								"senderId":senderId,
								"message":messageText,
								"isPostBackEvent": False
							}

							return resolvedData
					else:
						senderId = messaging_event["sender"]["id"]
						event_called = messaging_event["postback"]["payload"]
						resolvedData = {
							"senderId": senderId,
							"eventCalled": event_called,
							"isPostBackEvent": True
						}

						return resolvedData
