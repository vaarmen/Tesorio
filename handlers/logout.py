from handler import Handler

class LogoutHandler(Handler):
	def get(self):
		self.response.set_cookie('login', '')
		self.redirect('/')