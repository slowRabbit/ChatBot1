# This file contains the class to authenticate the user(currently via OTP)

class Authenticate:
    # Function to generate an OTP for a mobile number provided
    def generateOTP(self, number):

        # Function call to generate a new otp for the passed mobile number
        params["otpAttempt"] = 3
        return "Otp has been generated for the number"



    # Function to verify the otp passed by the user
    def verifyOtp(self, number, otp):

        # function call to get the otp generated for the number
        # if-else loop to check if generated otp and passed otp match

        return True

