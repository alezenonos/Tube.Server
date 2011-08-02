from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os

class main_page(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json"
        path = os.path.join(os.path.split(__file__)[0], 'formatted_distances.json')
        fares = open(path, "r")
        for line in fares:
            self.response.out.write(line)

application = webapp.WSGIApplication([('/get/distances', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()