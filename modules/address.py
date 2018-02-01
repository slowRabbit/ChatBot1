from event_invoker import EventInvoker
from handlers.events import EventHandler
from handlers.contexts import DialogFlowContextHandler

class AddressInquiry():

	def __init__(self, sessionId, account):
		self.session_id = sessionId
		self.eventInvoker = EventInvoker()
		self.eventHandler = EventHandler()
		self.dialogflow_context_handler = DialogFlowContextHandler()
		self.account = account

	def get_address(self):
		if(self.account.verified_account_number == ""):
			#invoke ASK_MOBILE_NUMBER_EVENT
			params = {
				"callerIntent":"VIEW_ADDRESS"
			}
			eventResponse = self.eventInvoker.invoke("ASK_MOBILE_NUMBER_EVENT", self.session_id, params)
			self.eventHandler.handle(eventResponse, self.session_id)
			return ["To proceed, we need to authenticate your account.", "Please enter your registered mobile number."]
		else:
			# fetchAddress()
		    self.dialogflow_context_handler.clear_context(self.session_id)
		    return "Business Bay,Pune"

	# Function to prompt the user to verify the address
	def ask_new_address(self):
		if(self.account.verified_account_number == ""):
			#invoke ASK_ACCOUNT_NUMBER
			params = {
				"callerIntent":"ASK_ADDRESS"
			}
			eventResponse = self.eventInvoker.invoke("ASK_MOBILE_NUMBER_EVENT", self.session_id, params)
			self.eventHandler.handle(eventResponse, self.session_id)
			return ["To proceed, we need to authenticate your account.", "Please enter your registered mobile number."]
		else:
			return "Please enter your new address"

	# Function to change address of the user
	def update_address(self, address):
		self.updated_address = address           # Database call will be made here to update the address field.
		confirmation_msg = "Your updated address is " + self.updated_address + "."
		self.dialogflow_context_handler.clear_context(self.session_id)
		return confirmation_msg