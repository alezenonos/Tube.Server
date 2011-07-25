from data.check_in_db import check_in_db
from data.check_in_db import check_in_db_key
from data.strings import tube_lines
from data.strings import tube_line_arrays
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import datetime
import logging

class Downloader(webapp.RequestHandler):
    def get(self):
        "Gets datum from an encoded url - will not be used, ideally"
        u=self.request.GET.get('user')
        o=self.request.GET.get('origin')
        d=self.request.GET.get('destination')
        t=self.request.GET.get('time')
        rd=self.request.GET.get('delay')
        rc=self.request.GET.get('crowd')
        rh=self.request.GET.get('happy')
        longi=self.request.GET.get('long')
        lat=self.request.GET.get('lat')
        c=self.request.GET.get('comment')

        l = self.find_line(o) + self.find_line(d)
        logging.info(l)
        
        database=check_in_db_key('check_in_database')
        check_in = check_in_db(parent=database, user=u, origin=o, destination=d, line=l, time_sent=t, rating_delay=rd, rating_crowded=rc, rating_happiness=rh, longitude=longi, latitude=lat, comment=c)
        check_in.put()
        logging.info("All data are extracted from the url")
        
    def find_line(self, queried):
        "Called to find on which line the stations fall"
        returned = list()
        for line_id in range(len(tube_line_arrays)):
            for station in tube_line_arrays[line_id]:
                if station==queried:
                    logging.info(tube_lines[line_id])
                    returned.append(tube_lines[line_id])
        return returned


application = webapp.WSGIApplication(
                                     [('/posted/here.*', Downloader) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()