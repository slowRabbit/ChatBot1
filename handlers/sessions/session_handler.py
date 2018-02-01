# This file contains the class to handle chat sessions(create new session if none exists or retrieve if one exists)

class SessionHandler:

    activeSessions = {}

    # Function to create a new chat session
    def addSession(self, sessionId, chatSession):
        self.activeSessions[sessionId] = chatSession
        pass

    # Function to check if an active session exists
    def fetchSession(self, sessionId):
        if sessionId in self.activeSessions:
            return True
        else:
            return False

    # Function to retrieve an existing chat session
    def retrieveSession(self, sessionId):
        return self.activeSessions[sessionId]