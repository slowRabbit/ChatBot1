from handlers.sessions import SessionHandler

class EventHandler:

	def __init__(self):
		self.sessionHandler = SessionHandler()

	def handle(self, response, sessionId):
		chatSession = self.sessionHandler.retrieveSession(sessionId)
		message = chatSession.get_response_to_event(response)
		return message