import requests
import json

class DialogFlowContextHandler():
    def clear_context(self, session_id):
    	headers = {
    		"Authorization": "Bearer 7eeb45b2cef942ca93c53c6a45fee576",
    		"Content-Type": "application/json"
    	}
    	data = json.dumps({
    		"sessionId" : session_id,
            "resetContexts" : "true",
            "query" : "let's start again",
            "lang" : "en"
    	})
    	response = requests.post("https://api.dialogflow.com/v1/query", headers=headers, data=data)
    	response = response.content