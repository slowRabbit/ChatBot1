from event_invoker import EventInvoker
from handlers.events import EventHandler

class AccountNumber():

    def __init__(self, sessionId):
        self.databaseVerified = False
        self.account_exists = False
        self.session_id = sessionId
        self.account_number_last_digits_input = "" # stores the last 4 digits of the account number as entered by the user
        self.input_account_number = ""   # stores the account number as selected by the user but not yet verified
        self.verified_account_number = "" # Verified Account number of the user
        self.otp_verification = False
        self.goto_intent_from_account = ""    # against caller event ASK_ACCOUNT_NUMBER_EVENT
        self.eventInvoker = EventInvoker()
        self.eventHandler = EventHandler()
        self.linked_account_numbers = []

    """
    set_goto_intent:
        reached through action call in AskAccountNumber intent or through event ASK_ACCOUNT_NUMBER_EVENT
        sets goto_intent variable for going back to ASK_ACCOUNT_NUMBER_EVENT caller intent
    """
    def set_goto_intent(self, caller_intent):
        #print "In action: AccountNumber.set_goto_intent called from", caller_intent
        self.goto_intent_from_account = caller_intent
        print self.goto_intent_from_account
        return "Please enter your account number"

    """
    confirm_account_number:
        reached through action call in GetAccountNumber intent or through event ACCOUNT_NOT_FOUND
        parses and confirms user input
    """
    # Function to parse user's message and extract account number from it
    def confirm_account_number(self, user_account_input, caller_intent_param):
        if type(user_account_input) is list:
            user_input = user_account_input[0]
        else:
            user_input = user_account_input
        input_digits = ''.join([i for i in user_input if i.isdigit()])
        last_four_digits = input_digits[-4:]
        #print "Parsed account number found is:", last_four_digits
        if(last_four_digits):
            self.account_number_last_digits_input = last_four_digits
            message = "Please confirm that you have entered " + self.account_number_last_digits_input + " as your account number?"
        else:
            message = ["What! Where are the digits?", "Please enter the last 4 digits of your account number"]
        return message


    """
    verify_account_number:
        reached through action call in ConfirmedAccountInput intent or through event VERIFY_ACCOUNT
        verifies account number locally & against database
        includes OTP verification call
    """
    def verify_account_number(self, caller_intent):
        if(caller_intent == "VERIFY_ACCOUNT"):
            otp_verification = True # Database call to verify OTP
            if otp_verification:
                self.verified_account_number= self.input_account_number
                messages = "Your account has been verified and authenticated."
            else:
                messages = "You have entered an incorrect OTP. Please try again!"
            # call event goto_intent_from_account with param "ASK_ACCOUNT_NUMBER"
            params={
                "callerIntent":"ASK_ACCOUNT_NUMBER"
            }
            if self.goto_intent_from_account:
                generatedResponse = []
                generatedResponse.append(messages)
                callEvent = self.goto_intent_from_account
                response = self.eventInvoker.invoke(callEvent, self.session_id, params)
                generatedResponse.append(self.eventHandler.handle(response, self.session_id))
                messages = generatedResponse
            return messages

        # input account number sanity check
        if(len(self.account_number_last_digits_input) == 4):
            for account_number in self.linked_account_numbers:
                last_four_digits = account_number[-4:]
                if self.account_number_last_digits_input == last_four_digits:
                    self.input_account_number = self.account_number_last_digits_input
                    self.account_exists = True

            if(self.account_exists):
                messages = "Please enter the OTP sent to your registered mobile number!"
            else:
                messages = "Oops! This account number is not registered with our database. Please try again!"
        else:
            messages = "Your need to enter the last 4 digits of your account nunber. Please try again!"

        params = {
            "callerIntent":"VERIFY_ACCOUNT"
        }

        # Check if account is verified from database and event to be called on dialogflow
        if(self.account_exists):
            callEvent = "OTP_SENDER"
        else:
            callEvent = "ACCOUNT_NOT_FOUND"
        self.eventInvoker.invoke(callEvent, self.session_id, params)
        return messages