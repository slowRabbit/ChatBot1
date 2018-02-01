import os.path
import sys
from constants import API_AI_CLIENT_ACCESS_TOKEN

try:
	import apiai
except ImportError:
	sys.path.append(
	os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
	)
	import apiai

class ApiAiInstanceCreator:
    def instantiate(self):
        CLIENT_ACCESS_TOKEN = API_AI_CLIENT_ACCESS_TOKEN
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        return ai