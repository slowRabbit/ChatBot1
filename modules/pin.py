from event_invoker import EventInvoker
from handlers.events import EventHandler
from handlers.contexts import DialogFlowContextHandler

class PinInquiry():

	def __init__(self, sessionId, account):
		self.eventInvoker = EventInvoker()
		self.eventHandler = EventHandler()
		self.dialogflow_context_handler = DialogFlowContextHandler()
		self.account = account
		self.sessionId = sessionId

	# Function to prompt the user for a new pin and to check if account details exist
	def ask_new_pin(self):
		if(self.account.verified_account_number == ""):
			#invoke ASK_ACCOUNT_NUMBER
			params = {
				"callerIntent":"ASK_PIN"
			}
			eventResponse = self.eventInvoker.invoke("ASK_MOBILE_NUMBER_EVENT", self.sessionId, params)
			message = self.eventHandler.handle(eventResponse, self.sessionId)
			return ["To proceed, we need to authenticate your account.", "Please enter your account number."]
		else:
			return "Please enter your new PIN"

	# Function to save the new pin
	def update_pin(self, pin_message):
		if type(pin_message) is list:
			pin_input = pin_message[0]
		else:
			pin_input = pin_message

		pin_digits = ''.join([i for i in pin_input if i.isdigit()])
		last_6_digits = pin_digits[-6:]

		if(len(last_6_digits)==6):
			self.updated_pin = last_6_digits
			self.dialogflow_context_handler.clear_context(self.session_id)
			message = "Your updated PIN is " + self.updated_pin + "."
		else:
			message = ["What! Where are the digits?", "Please enter a 6-digit PIN"]

		# Database call will be made here to update the address field.
		return message