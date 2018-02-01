import json
from event_invoker import EventInvoker
from handlers.events import EventHandler
from handlers.contexts import DialogFlowContextHandler

class BalanceInquiry:

    def __init__(self, sessionId):
        self.session_id = sessionId
        self.eventHandler = EventHandler()
        self.eventInvoker = EventInvoker()
        self.dialogflow_context_handler = DialogFlowContextHandler()

    def get_balance(self, account):
        self.account = account
        if(self.account.verified_account_number == ""):
            #invoke ASK_ACCOUNT_NUMBER
            params = {
                "callerIntent":"GET_BALANCE"
            }
            eventResponse = self.eventInvoker.invoke("ASK_MOBILE_NUMBER_EVENT", self.session_id, params)
            message = self.eventHandler.handle(eventResponse, self.session_id)
            return ["To proceed, we need to authenticate your account.", "Please enter your registered mobile number."]
        else:
            # fetchBalance()
		    self.dialogflow_context_handler.clear_context(self.session_id)
		    return "Your account balance is Rs. 2000"