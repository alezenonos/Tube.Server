from data.check_in_db import check_in_db_key, check_in_db
from data.user_db import user_db
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

#def get_understandable_users(self, entries):
#    "gets more readable identifiers for printing"
#    returned_list = dict()
#    for entry in entries:
#        returned_list[entry.user] = user_db.get([entry.user]).twitter_id
#    return entries

class main_page(webapp.RequestHandler):
    def get(self):
        logging.info("start of get")
        entry_query = check_in_db.all().ancestor(check_in_db_key('check_in_database')).order("-time_sent")
        entries = entry_query.fetch(100)
        template_values = {
            'entries': entries,
#            'users' : get_understandable_users(self, entries),
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