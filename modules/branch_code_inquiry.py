import json
from event_invoker import EventInvoker
from handlers.events import EventHandler

class BranchCodeInquiry:

    def __init__(self, sessionId, account):
        self.session_id = sessionId
        self.eventHandler = EventHandler()
        self.eventInvoker = EventInvoker()
        self.account = account

    def get_branch_code(self, branch):
        if(self.account.verified_account_number == ""):
            #invoke ASK_ACCOUNT_NUMBER
            params = {
                "callerIntent":"BANK_CODE"
            }
            eventResponse = self.eventInvoker.invoke("ASK_ACCOUNT_NUMBER_EVENT", self.session_id, params)
            message = self.eventHandler.handle(eventResponse, self.session_id)
            return ["To proceed, we need to authenticate your account.", "Please enter your account number."]
        else:
            #  branchCode = fetchBranchCode()
            return " Branch Code is 12345. "