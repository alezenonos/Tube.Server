from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os

version_number = 3

class fares_downloader(webapp.RequestHandler):
    "accessed by the client to download the current fares"
    def get(self):
        self.response.headers['Content-Type'] = "application/json"
        path = os.path.join(os.path.split(__file__)[0], 'formatted_fares.json')
        fares = open(path, "r")
        for line in fares:
            self.response.out.write(line)
            
class fares_version(webapp.RequestHandler):
    "for the client to check to see if it needs to download the fares"
    def get(self):
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("Fares Version Number: " + str(version_number))
            
            
application = webapp.WSGIApplication(
                                     [
                                      ('/get/fares', fares_downloader),
                                      ('/get/fares/ver', fares_version)
                                      ],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()