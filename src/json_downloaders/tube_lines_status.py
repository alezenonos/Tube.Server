from data.check_in_db import check_in_db_key
from data.strings import tube_lines
from data.user_db import user_db
from datetime import datetime
from django.utils import simplejson as json
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class main_page(webapp.RequestHandler):
    present = datetime.now()
    one_hours_past = present.replace(hour=(present.hour-1))
    three_hours_past = present.replace(hour=(present.hour-3))
    
    def get(self):
        self.response.headers['Content-Type'] = "application/json"
        printable_status = dict.fromkeys(tube_lines)
        for index in range(len(tube_lines)):
            gotten_average = self.get_average(tube_lines[index], False)
            if gotten_average == -1:
                printable_status[tube_lines[index]] = None
            else:
                printable_status[tube_lines[index]] = gotten_average
        
        self.response.out.write(json.dumps(printable_status, sort_keys=True, indent=4 ))
    
    def get_average(self, line, threehours):
        "Returns entries from the database, depending on the given line"
        if threehours is False:
            past = self.one_hours_past
        else:
            past = self.three_hours_past
            
        time_query = db.GqlQuery("SELECT * "
                         "FROM check_in_db "
                         "WHERE ANCESTOR IS :1 AND time_sent > :2 AND line = :3 "
                         "ORDER BY time_sent",
                         check_in_db_key('check_in_database'),
                         past,
                         line)

        entries = time_query.fetch(500)
        
        if (len(entries) == 0):
            if (threehours is False):
                return self.get_average(line, True)
            else:
                return -1
        else:
            if (len(entries) < 10) and (threehours is False):
                return self.get_average(line, True)
            else:        
                return self.compute_averages(entries, threehours)

    def compute_averages(self, entries, threehours):
        average_rating_delay = 0
        average_rating_crowded = 0
        average_rating_happiness = 0
        users = []
        for entry in entries:
            average_rating_delay += entry.rating_delay
            average_rating_crowded += entry.rating_crowded
            average_rating_happiness += entry.rating_happiness
            if not (entry.user.key() in users):
                users.append(entry.user.key())
            
        return dict({
                     'rating':average_rating_delay/len(entries), 
                     'crowded':average_rating_crowded/len(entries), 
                     'happiness':average_rating_happiness/len(entries),
                     'users':len(users),
                     'threehours':threehours,
                     'entries':len(entries)
                     })

def main():
    application = webapp.WSGIApplication([('/get/tube-lines-status', main_page)], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()