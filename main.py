# the import section
import webapp2
import os
import jinja2
import random
from google.appengine.api import users

# this initializes the jinja2 environment
# this will be the same in every app that uses the jinja2 templating library 
jinja_current_directory = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

# other functions should go above the handlers or in a separate file

# the handler section
class LoginHandler(webapp2.RequestHandler):
  def get(self):  # for a get request
    login_template = jinja_current_directory.get_template("templates/login.html")
    self.response.write(login_template.render())

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    home_template = jinja_current_directory.get_template("templates/home.html")
    self.response.write(home_template.render())

class AboutHandler(webapp2.RequestHandler):
  def get(self):
    about_template = jinja_current_directory.get_template("templates/about.html")
    self.response.write(about_template.render())


# the app configuration section	
app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/about', AboutHandler),
  ('/login', LoginHandler),
  ('/home', HomeHandler),
], debug=True)