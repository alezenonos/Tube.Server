from data.user_db import user_db, user_db_key
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import os

url_back_home = '/'
url_text = 'Home'
datastore = 'users'

class main_page(webapp.RequestHandler):
    def get(self):
        logging.info("start of get")
        entry_query = user_db.all().ancestor(user_db_key('user_database'))
        entries = entry_query.fetch(100)
        template_values = {
            'entries': entries,
            'datastore' : datastore,
            'url_home' : url_back_home,
            'url_linktext' : url_text
        }
        path = os.path.join(os.path.dirname(__file__), 'print_users_layout.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/users', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()