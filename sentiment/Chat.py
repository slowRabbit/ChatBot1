# this is the object class(model) for a chat message, 

class Chat:
    
    #chat 
    #time 
    #score
    #magnitude
    #factor = score * magnitude
    
    def __init__(self, chat, time, score, magnitude, factor):
        self.chat = chat
        self.time = time
        self.score = score
        self.magnitude = magnitude
        self.factor = factor
    
    def getChat(self):
        return self.chat
    
    def getTime(self):
        return self.time
    
    def getScore(self):
        return self.score
    
    def getMagnitude(self):
        return self.magnitude
    
    def getFactor(self):
        return self.factor