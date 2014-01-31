import webapp2
import os
import jinja2

import models

template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class IndexHandler(Handler):
    def get(self):
        self.redirect("/panel")

class PanelHandler(Handler):
    def get(self):
        self.render("html/upload-company2.html")

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/panel', PanelHandler)
], debug=True)
