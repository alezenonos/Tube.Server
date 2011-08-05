from data.user_db import user_db_key
from data.log_db import log_db
from data.log_db import log_db_key
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import datetime
import csv
import os

class get_csv(webapp.RequestHandler):
    "gets csv logs from client"
    def get(self):
#    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<html><body>')
        
        #for testing
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "sent_testfile.csv"))
        test_csv = csv.reader(open(path))
        self.process(test_csv)
        
        #for actual eventual usage
#        received_csv = self.request.body
#        self.process(received_csv)
        
        self.response.out.write('</body></html>')
        
    def process(self, received_csv):
        "processes the csv into the log files"
#        self.response.out.write(csv)
        list_of_entities = []
        metadata = received_csv.next()
        user_key = self.get_user_key_from_database(metadata[1], metadata[0])
        log_ts = datetime.strptime(metadata[2], '%Y-%m-%d %H:%M:%S')
        if user_key is not None:
            self.response.out.write("<p>User Key: <i>" + str(user_key) + "</i></p>")
            self.response.out.write("<p>Log time-stamp: <i>" + str(log_ts) + "</i></p>")
            for row in received_csv:
                activity_ts = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                list_of_entities.append(
                                        log_db(
                                               parent=log_db_key('log_database'),
                                               user=user_key,
                                               log_time_stamp=log_ts,
                                               activity_time_stamp=activity_ts,
                                               content=row[1]
                                               )
                                        )
                self.response.out.write("<p>Activity time-stamp: <i>" + str(activity_ts) + "</i></p>")
                self.response.out.write("<p>Content of log: <i>" + str(row[1]) + "</i></p><hr>")
            db.put(list_of_entities)
        else:
            self.response.out.write("<p><i>Error: User not found</i></p>")
            
            
    def get_user_key_from_database(self, user_id, account):
        "returns the key of the requested user in the database"
        returned_user = None
        if account == 'twitter':
            returned_user = self.check_twitter_user(user_id)
        else:
            returned_user = self.check_facebook_user(user_id)
        if len(returned_user) > 0:
            return returned_user[0]
    
    def check_twitter_user(self, twitter_id):
        query = db.GqlQuery(
                            "SELECT __key__ "
                            "FROM user_db "
                            "WHERE ANCESTOR IS :1 AND twitter_id = :2",
                            user_db_key('user_database'),
                            twitter_id
                            )
        return query.fetch(1)
    
    def check_facebook_user(self, facebook_id):
        query = db.GqlQuery(
                            "SELECT __key__ "
                            "FROM user_db "
                            "WHERE ANCESTOR IS :1 AND facebook_id = :2",
                            user_db_key('user_database'),
                            facebook_id
                            )
        return query.fetch(1)
        
        

def main():
    application = webapp.WSGIApplication([('/upload/csv', get_csv)], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
