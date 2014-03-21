from handler import Handler

class LogoutHandler(Handler):
	def get(self):
		self.auth.unset_session()
		self.redirect('/login')