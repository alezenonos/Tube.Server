from data.check_in_db import check_in_db_key, check_in_db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from datetime import datetime
import logging
import os

url_back_home = '/'
url_text = 'Home'
datastore = 'check-ins'

class main_page(webapp.RequestHandler):
    def get(self):
        logging.info("start of get")
        entry_query = check_in_db.all().ancestor(check_in_db_key('check_in_database'))
        entries = entry_query.fetch(100)
        template_values = {
            'entries': entries,
            'datastore' : datastore,
            'url_home' : url_back_home,
            'url_linktext' : url_text
        }
        path = os.path.join(os.path.dirname(__file__), 'print_check_in_layout.html')
        self.response.out.write(template.render(path, template_values))
        
#        check_in_db(parent=check_in_db_key('check_in_database'),origin=1,destination=2,line=8,time_sent=datetime.now(),rating_delay=db.Rating(15),rating_crowded=db.Rating(25)).put()

application = webapp.WSGIApplication([('/check-in', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()