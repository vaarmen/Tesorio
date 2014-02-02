from handler import Handler

class IndexHandler(Handler):
    def get(self):
        self.write("Lol")