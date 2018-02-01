from event_invoker import EventInvoker
from handlers.events import EventHandler

class MobileNumber():

    def __init__(self, sessionId, accountNumber):
        self.account = accountNumber
        self.databaseVerified = False
        self.db_response = False
        self.session_id = sessionId
        self.input_mobile_number = ""   # maintain the last input
        self.verified_mobile_number = "" # Verified Account number of the user
        self.goto_intent = ""    # against caller event ASK_ACCOUNT_NUMBER_EVENT
        self.eventInvoker = EventInvoker()
        self.eventHandler = EventHandler()


    # Function to prompt the user to enter their mobile number
    def ask_mobile_number(self, caller_intent):
        self.goto_intent = caller_intent
        return "Please enter your registered mobile number"


    # Function to parse user's message and extract mobile number from it
    def confirm_mobile_number(self, user_number_input, caller_intent_param):
        if type(user_number_input) is list:
            user_input = user_account_input[0]
        else:
            user_input = user_number_input
        input_digits = ''.join([i for i in user_input if i.isdigit()])
        last_10_digits = input_digits[-10:]
        #print "Parsed account number found is:", last_12_digits
        if(last_10_digits):
            self.input_mobile_number = last_10_digits
            message = "Please confirm that you have entered " + self.input_mobile_number + " as your registered mobile number?"
        else:
            message = ["What! Where are the digits?", "Please enter 10-digit mobile number"]
        return message



    # Function to verify the mobile number from the database
    def verify_mobile_number(self, caller_intent):
        # input mobile number sanity check
        if(len(self.input_mobile_number) == 10):
            self.db_response = True # Database call to verify mobile number

            if(self.db_response):
                messages = "Please enter the last four digits of your account number"
                self.account.linked_account_numbers = self.getLinkedAccountNumbers()
                self.databaseVerified = True
            else:
                messages = "Oops! This mobile number is not registered with our database. Please try again!"
        else:
            messages = "Your mobile number must be 10 digits long. Please try again!"

        # Check if mobile number is verified from database and event to be called on dialogflow
        if(self.databaseVerified):
            params = {
                "callerIntent":self.goto_intent
            }
            callEvent = "ASK_ACCOUNT_NUMBER_EVENT"
            eventResponse = self.eventInvoker.invoke(callEvent, self.session_id, params)
            message = self.eventHandler.handle(eventResponse, self.session_id)
            print ""
        else:
            params = {
                "callerIntent":"VERIFY_MOBILE_NUMBER"
            }
            callEvent = "ACCOUNT_NOT_FOUND"
            self.eventInvoker.invoke(callEvent, self.session_id, params)
        return messages

    # Function to get the account numbers linked with the mobile number
    def getLinkedAccountNumbers(self):
        return ["123456789012", "210987654321"]