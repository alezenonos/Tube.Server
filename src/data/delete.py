from data.log_db import log_db, log_db_key
from data.user_db import user_db
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
import logging

class main_page(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<html><body>')
        logging.info('Starting')
        query = log_db.all().ancestor(log_db_key('log_database'))
#        while len(query.fetch(1)) > 0:
        for a in range(20):
            logging.info('round ' + str(a))
            entries = query.fetch(500)
            for entry in entries:
                self.response.out.write("<p>User Key: <i>" + str(entry.user.key()) + "</i></p>")
                self.response.out.write("<p>Log time-stamp: <i>" + str(entry.log_time_stamp) + "</i></p>")
                self.response.out.write("<p>Activity time-stamp: <i>" + str(entry.activity_time_stamp) + "</i></p>")
                self.response.out.write("<p>Content of log: <i>" + str(entry.content) + "</i></p><hr>")
                db.delete(entry)
                self.response.out.write("<p><i>~~~deleted</i></p><hr>")
        self.response.out.write('</body></html>')
                
application = webapp.WSGIApplication(
                                     [('/delete/logs', main_page) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()