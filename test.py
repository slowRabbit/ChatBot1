import urllib2
import json
        
data = {
        'time':'23:45',
        'chat':'how are you'
        }

req = urllib2.Request('https://chat-sentiment-analyzer.herokuapp.com/postChat')
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(data))
response = response.read()
jsonResponse = json.loads(response)

print (response)