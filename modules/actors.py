from balance_inquiry import BalanceInquiry
from mobile_number import MobileNumber
from account_number import AccountNumber
from address import AddressInquiry
from pin import PinInquiry
from lost_card import LostCard
from branch_code_inquiry import BranchCodeInquiry
from contact_agent import ContactAgent

class Actors:

    def __init__(self, sessionId):
        self.session_id = sessionId
        self.accountNumber = AccountNumber(self.session_id)
        self.mobile_number = MobileNumber(self.session_id, self.accountNumber)
        self.balanceInquiry = BalanceInquiry(self.session_id)
        self.address_inquiry = AddressInquiry(self.session_id, self.accountNumber)
        self.pin_inquiry = PinInquiry(self.session_id, self.accountNumber)
        self.lost_card = LostCard(self.session_id, self.accountNumber)
        self.branchCodeInquiry = BranchCodeInquiry(self.session_id, self.accountNumber)
        self.contactAgent = ContactAgent(self.session_id)

    def act(self, actorIndex, response):

        if (actorIndex == 0):
            caller_intent = response['result']['parameters']['callerIntent']
            message = self.mobile_number.ask_mobile_number(caller_intent)

        elif(actorIndex == 1):
            caller_intent = response['result']['parameters']['callerIntent']
            input_mobile_number = response['result']['parameters']['mbno']
            message = self.mobile_number.confirm_mobile_number(input_mobile_number, caller_intent)

        elif (actorIndex == 2):
            self.mobile_number.input_mobile_number = ""
            message = ["Oh! Seems like I messed up!", "Please re-enter your registered mobile number."]

        elif (actorIndex == 3):
            caller_intent = response['result']['parameters']['callerIntent']
            message = self.mobile_number.verify_mobile_number(caller_intent)

        elif (actorIndex == 4):
            caller_intent = response['result']['parameters']['callerIntent']
            message = self.accountNumber.set_goto_intent(caller_intent)

        elif (actorIndex == 5):
            account_number_last_digits_input = response['result']['parameters']['accNumber']
            caller_intent = response['result']['parameters']['callerIntent']
            message = self.accountNumber.confirm_account_number(account_number_last_digits_input, caller_intent)

        elif (actorIndex == 6):
            self.accountNumber.input_account_number = ""
            self.accountNumber.account_number_last_digits_input = ""
            message = "Oh! Seems like I messed up, or, did you?"

        elif (actorIndex == 7):
            caller_intent = response['result']['parameters']['callerIntent']
            message = self.accountNumber.verify_account_number(caller_intent)

        elif (actorIndex == 8):
            caller_intent = response['result']['parameters']['callerIntent']
            message = self.accountNumber.verify_account_number(caller_intent)

        elif (actorIndex == 9):
            message = self.balanceInquiry.get_balance(self.accountNumber)

        elif (actorIndex == 10):
            message = self.address_inquiry.get_address()

        elif (actorIndex == 11):
            message = self.address_inquiry.ask_new_address()

        elif (actorIndex == 12):
            address = response['result']['parameters']['address']
            message = self.address_inquiry.update_address(address)

        elif (actorIndex == 13):
            message = self.pin_inquiry.ask_new_pin()

        elif (actorIndex == 14):
            pin = response['result']['parameters']['pin']
            message = self.pin_inquiry.update_pin(pin)

        elif (actorIndex == 15):
            message = self.lost_card.get_card_number()

        elif (actorIndex == 16):
            cardNumber = response['result']['parameters']['cardNumber']
            message = self.lost_card.verify_card_number(cardNumber)

        elif (actorIndex == 17):
            cvv = response['result']['parameters']['cvv']
            message = self.lost_card.verify_cvv(cvv)

        elif (actorIndex == 18):
            branch = response['result']['parameters']['branch']
            message = self.branchCodeInquiry.get_branch_code(self.branch)

        elif (actorIndex == 100):
            message = response['result']['fulfillment']['speech']
            self.contactAgent.call(response)

        else:
            return "Undefined Action"

        return message