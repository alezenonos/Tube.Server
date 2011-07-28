from data.check_in_db import check_in_db_key
from data.strings import tube_lines
from datetime import datetime
from django.utils import simplejson as json
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging

class main_page(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json"
        printable_status = dict.fromkeys(tube_lines)
        for index in range(len(tube_lines)):
            gotten_average = self.get_average(tube_lines[index], 0)
            if gotten_average == -1:
                printable_status[tube_lines[index]] ='No Ratings Available'
            else:
                printable_status[tube_lines[index]] = gotten_average
        
        self.response.out.write(json.dumps(printable_status, sort_keys=True, indent=4 ))
    
    def get_average(self, line, threehours):
        "Returns entries from the database, depending on the given line"
        present = datetime.now()
        logging.info(present)
        
        if threehours == 1:
            logging.info('getting one hour')
            past = present.replace(hour=(present.hour-1))
        else:
            logging.info('getting three hours')
            past = present.replace(hour=(present.hour-3))
            
        time_query = db.GqlQuery("SELECT * "
                         "FROM check_in_db "
                         "WHERE ANCESTOR IS :1 AND time_sent > :2 AND line = :3 "
                         "ORDER BY time_sent",
                         check_in_db_key('check_in_database'),
                         past,
                         line)

        entries = time_query.fetch(500)
        logging.info('length of entries')
        logging.info(len(entries))
        
        if (len(entries) == 0):
            logging.info('returning -1')
            return -1
        else:
            if (len(entries) < 10):
                if (threehours == 0):
                    return self.get_average(line, 1)
                else:
                    return self.compute_averages(entries)
            else:        
                return self.compute_averages(entries)

    def compute_averages(self, entries):
        average_rating_delay = 0
        average_rating_crowded = 0
        average_rating_happiness = 0
        for entry in entries:
            average_rating_delay += entry.rating_delay
            average_rating_crowded += entry.rating_crowded
            average_rating_happiness += entry.rating_happiness
            logging.info(average_rating_delay)
            logging.info(average_rating_crowded)
            logging.info(average_rating_happiness)
            
        return dict({
                     'rating':average_rating_delay/len(entries), 
                     'crowded':average_rating_crowded/len(entries), 
                     'happiness':average_rating_happiness/len(entries)
                     })

def main():
    application = webapp.WSGIApplication([('/get/tube-lines-status', main_page)], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()