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

def main(args=None):
    msg = "Download song lyrics from Genius.com"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("search_type", type=str.lower, choices=["song", "artist"],
                        help="Specify whether search is for 'song' or 'artist'")
    parser.add_argument("terms", type=str, nargs="+",
                        help="Provide terms for search")
    parser.add_argument("--save", action="store_true",
                        help="If specified, saves songs to JSON file")
    parser.add_argument("--max-songs", type=int,
                        help="Specify number of songs when searching for artist")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Turn off the API verbosity")
    args = parser.parse_args()

    # Create an instance of the Genius class
    client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
    msg = "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN"
    assert client_access_token, msg
    api = Genius(client_access_token)
    if args.quiet:
        api.verbose = False

    # Handle the command-line inputs
    if args.search_type == "song":
        song = api.search_song(*args.terms)
        if not song:
            if not args.quiet:
                print("Could not find specified song. Check spelling?")
            return
        if args.save:
            if not args.quiet:
                print("Saving lyrics to '{s}'...".format(s=song.title))
            song.save_lyrics()
    else:
        artist = api.search_artist(args.terms[0],
                                   max_songs=args.max_songs,
                                   sort='popularity')
        if args.save:
            if not args.quiet:
                print("Saving '{a}'' lyrics...".format(a=artist.name))
            api.save_artists(artist)


if __name__ == "__main__":
    main()

# the app configuration section	
app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/about', AboutHandler),
  ('/login', LoginHandler),
  ('/home', HomeHandler),
], debug=True)