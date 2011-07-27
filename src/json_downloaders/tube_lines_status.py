from data.check_in_db import check_in_db_key
from data.strings import tube_lines
from datetime import datetime
from django.utils import simplejson as json
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class main_page(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json"
        printable_status = dict.fromkeys(tube_lines)
        for index in range(len(tube_lines)):
            gotten_average = self.get_average(index)
            if gotten_average == -1:
                printable_status[tube_lines[index]] ='No Ratings Available'
            else:
                printable_status[tube_lines[index]] = gotten_average
        
        self.response.out.write(json.dumps(printable_status, sort_keys=True, indent=4 ))
    
    def get_average(self, line):
        "Returns entries from the database, depending on the given line"
        now = datetime.now()
        hour_ago = now.replace(hour=(now.hour-1))
        time_query = db.GqlQuery("SELECT * "
                                 "FROM check_in_db "
                                 "WHERE ANCESTOR IS :1 AND time_sent > :2 AND line = :3 "
                                 "ORDER BY time_sent",
                                 check_in_db_key('check_in_database'),
                                 hour_ago,
                                 line)
        entries = time_query.fetch(500)
        
        if (len(entries) == 0):
            return -1
        else:        
            average_rating_delay = 0
            average_rating_crowded = 0
            for entry in entries:
                average_rating_delay += entry.rating_delay
                average_rating_crowded += entry.rating_crowded
            return dict({'rating':average_rating_delay/len(entries), 'crowded':average_rating_crowded/len(entries)})

application = webapp.WSGIApplication([('/get/tube-lines-status', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()