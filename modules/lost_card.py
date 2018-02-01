from account_number import AccountNumber
from event_invoker import EventInvoker
from handlers.events import EventHandler
from handlers.contexts import DialogFlowContextHandler

eventInvoker = EventInvoker()

class LostCard():

	def __init__(self, sessionId, account):
		self.session_id = sessionId
		self.eventInvoker = EventInvoker()
		self.eventHandler = EventHandler()
		self.dialogflow_context_handler = DialogFlowContextHandler()
		self.account = account
		self.card_verified = False
		self.cvv_verified = False

	def get_card_number(self):
		if(self.account.verified_account_number == ""):
			#invoke ASK_ACCOUNT_NUMBER
			params = {
			"callerIntent":"LOST_CARD"
			}
			eventResponse = self.eventInvoker.invoke("ASK_MOBILE_NUMBER_EVENT", self.session_id, params)
			self.eventHandler.handle(eventResponse, self.session_id)
			return ["To proceed, we need to authenticate your account.", "Please enter your registered mobile number."]
		else:
			return "Please enter the last four digits of your Card"

	def verify_card_number(self, card_number):
		 self.card_verified = True #findCardNumber(cardNumber);
		 params = {
		 "callerIntent":"ASK_CARD_NUMBER"
		 }

		 if self.card_verified == False:
			#response = eventInvoker.invoke("ASK_CARD_NUMBER", self.session_id, params)
			return "Your card number does not exist. Please enter the last four digits your card number again."
		 else:
			response = eventInvoker.invoke("ASK_CVV", self.session_id, params)    #will it go directly there or we need to call that event explictly
			return "Please enter your CVV"
			#return response

	def verify_cvv(self, cvv):
		self.cvv_verified = True # findCVV(cvv);
		#invoke ASK_ACCOUNT_NUMBER
		params = {
		"callerIntent":"ASK_CVV"
		}
		if self.card_verified == False:
			#response = eventInvoker.invoke("ASK_CVV", self.session_id, params)
			return "Your CVV  does not exist.Please enter your CVV again."
		else:
		    self.dialogflow_context_handler.clear_context(self.session_id)
		    return "Your card has been successfully blocked!"