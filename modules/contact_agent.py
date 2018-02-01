import requests
import json

class ContactAgent:
    def __init__(self, sessionId):
        self.session_id = sessionId

    def call(self, message):
        params = {
            "access_token": "EAAEkyBZC1iZBMBAO43btZBfdy9hf9sitn0BNnXCbtRkzT0ZA84aPCrRSkZB00tFIzrijQGsGoi8oBoputQ6pZCPwlx3oMGI3QCRIDm4uApsKKVR02dtBDsZCbmlLNFNpjgb7EkeZBj0iUhE02VTgutGhdyscIdzHcxHs6yYGKKw4HAZDZD"
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient":{
                "id":self.session_id
            },
            "message":{
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":"Tap the below button to get in touch with an agent.",
                        "buttons":[
                            {
                                "type":"phone_number",
                                "title":"Speak now",
                                "payload":"18602662667"
                            }
                        ]
                    }
                }
            }
        })
        response = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        response = response.content
        print response