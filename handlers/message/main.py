# This file contains the class to handle incoming messages, extract data from them
# and return back for processing

from facebook_messenger import FacebookHandler

class MessageHandler:

	# Function to handle incoming messages
	def handle(self, data, platform):

		# Getting resolved data based on the platform
		if platform == 'facebook':
			facebookHandler = FacebookHandler()
			resolvedData = facebookHandler.getData(data)

		return resolvedData