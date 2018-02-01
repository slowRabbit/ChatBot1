from actors import Actors

class Router:

    def __init__(self, sessionId):
        self.sessionId = sessionId
        self.actors = Actors(self.sessionId)
        self.next_expected_action = []

    def getActionIndex(self, action):
        if action in self.routerMappings:
            return self.routerMappings[action]["actorIndex"]
        else:
            return -1

    def get_next_expected_actions(self, action):
        if action in self.routerMappings:
            return self.routerMappings[action]["nextActionExpected"]
        else:
            return []

    def route(self, response):
        action = response['result']['action']
        print "Calling action - ",action
        actorIndex = self.getActionIndex(action)
        if(actorIndex==-1):
            responseMsgs = response['result']['fulfillment']['speech']
        else:
            self.next_expected_action = self.get_next_expected_actions(action)
            print "Next action expected - ", self.next_expected_action
            responseMsgs = self.actors.act(actorIndex, response)

        print responseMsgs
        return responseMsgs

    def is_expected_action(self, action):
        if action in self.next_expected_action:
            return True
        else:
            return False

    routerMappings = {
        # Maps to function to set next Intent post data input from user
        "askMobileNumber" : {
            "actorIndex" : 0,
            "nextActionExpected" : ["confirmMobileNumber"]
        },

        # Maps to function to set next Intent post data input from user
        "confirmMobileNumber" : {
            "actorIndex" : 1,
            "nextActionExpected" : ["denyMobileNumberInput", "verifyMobileNumber"]
        },

        # Maps to function to set next Intent post data input from user
        "denyMobileNumberInput" : {
            "actorIndex" : 2,
            "nextActionExpected" : ["confirmMobileNumber"]
        },

        # Maps to function to set next Intent post data input from user
        "verifyMobileNumber" : {
            "actorIndex" : 3,
            "nextActionExpected" : ["setGotoIntent"]
        },

        # Maps to function to set next Intent post data input from user
        "setGotoIntent" : {
            "actorIndex" : 4,
            "nextActionExpected" : ["confirmAccountNumber"]
        },

        # Maps to function to prompt account number confirmation
        "confirmAccountNumber" : {
            "actorIndex" : 5,
            "nextActionExpected" : ["deniedAccountNumber", "verifyAccountNumber"]
        },

        # Maps to function to prompt to enter account number again
        "deniedAccountNumber" : {
            "actorIndex" : 6,
            "nextActionExpected" : ["confirmAccountNumber"]
        },

        # Maps to function to verify account number, once confirmed by user
        "verifyAccountNumber" : {
            "actorIndex" : 7,
            "nextActionExpected" : ["verifyOTPInput"]
        },

        # Maps to function to verify OTP sent to the user's registered mobile number
        "verifyOTPInput" : {
            "actorIndex" : 8,
            "nextActionExpected" : []
        },

        # Maps to function to get user's account balance
        "getBalance" : {
            "actorIndex" : 9,
            "nextActionExpected" : ["", "askMobileNumber"]
        },

        # Maps to function to get address
        "getAddress" : {
            "actorIndex" : 10,
            "nextActionExpected" : ["", "setGotoIntent"]
        },

        # Maps to function to verify account for address change
        "verifyAccountAddress" : {
            "actorIndex" : 11,
            "nextActionExpected" : ["editAddress"]
        },

        # Maps to function to change address
        "editAddress" : {
            "actorIndex" : 12,
            "nextActionExpected" : ["confirmAccountNumber"]
        },

        # Maps to function to verify account for PIN change
        "verifyAccountPIN" : {
            "actorIndex" : 13,
            "nextActionExpected" : ["editPIN"]
        },

        # Maps to function to change PIN
        "editPIN" : {
            "actorIndex" : 14,
            "nextActionExpected" : ["confirmAccountNumber"]
        },

        # Maps to verify account to report Lost card
        "verifyAccountLostCard" : {
            "actorIndex" : 15,
            "nextActionExpected" : ["verifyCardNumber"]
        },

        # Maps to verify if card number exist for it's respective account number
        "verifyCardNumber" : {
            "actorIndex" : 16,
            "nextActionExpected" : ["verifyCVV"]
        },

        # Maps to verify if CVV exist for it's respective account number
        "verifyCVV" : {
            "actorIndex" : 17,
            "nextActionExpected" : []
        },

        # Maps to funtion which returns bank code
        "bankCode" : {
            "actorIndex" : 18,
            "nextActionExpected" : ["", "setGotoIntent"]
        },

        "contactHuman" : {
            "actorIndex" : 100,
             "nextActionExpected" : [""]
        }

    }