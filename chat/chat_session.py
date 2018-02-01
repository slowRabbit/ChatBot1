import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chat import Chat
from handlers.sessions import SessionHandler

class ChatSession:
	def __init__(self):
		self.sessionHandler = SessionHandler()

	def getChatSession(self, senderId):
		# Checking & retrieving an active chat session & creating if none exists
		if self.sessionHandler.fetchSession(senderId):
			chatSession = self.sessionHandler.retrieveSession(senderId)
		else:
			chatSession = Chat(senderId)
			self.sessionHandler.addSession(senderId, chatSession)
		return chatSession