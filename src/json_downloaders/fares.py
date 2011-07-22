from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import re
import os

class main_page(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.split(__file__)[0], 'parsed.json')
        fares = open(path, "r")
        for line in fares:
            print line

application = webapp.WSGIApplication([('/get/fares', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()