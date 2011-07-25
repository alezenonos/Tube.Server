from data.check_in_db import check_in_db
from data.check_in_db import check_in_db_key
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging

class Downloader(webapp.RequestHandler):
    
    def get(self):
        database=check_in_db_key('check_in_database')
#        check_in = check_in_db(parent=database)
        u=self.request.GET.get('user')
        o=self.request.GET.get('origin')
        d=self.request.GET.get('destination')
        t=self.request.GET.get('time')
        rd=self.request.GET.get('delay')
        rc=self.request.GET.get('crowd')
        rh=self.request.GET.get('happy')
        c=self.request.GET.get('comment')
        check_in = check_in_db(parent=database, user=u, origin=o, destination=d, time_sent=t, rating_delay=rd, rating_crowded=rc, rating_happiness=rh, comment=c)
        check_in.put()
        logging.info(u)
        logging.info("All data are extracted from the url")
#        check_in.put()
        
        
application = webapp.WSGIApplication(
                                     [('/posted/here.*', Downloader) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()