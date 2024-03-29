from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache
from django.utils import simplejson as json
from test_uploader.receive_check_ins import add_to_check_in_db
from test_uploader.receive_reports import add_to_reports_db
from test_uploader.receive_user import add_to_user_db
from test_uploader.receive_user import update_user_in_db
from data.check_in_db import check_in_db_key
from data.report_db import report_db_key
from data.user_db import user_db_key
from datetime import datetime
import logging 

class get_raw(webapp.RequestHandler):
    "gets the raw submitted data from the client"
    def post(self):
#    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write('<html><body>')
#        parsed_json = json.loads(json.dumps({"check_in":{"time_stamp":"2984-07-31 08:25:11","delay":2,"twitter":"neal_lathia","message":"","crowd":2,"latitude":"51.5315581","longitude":"-0.13440335","origin":"Euston","modality":"tube","destination":"Liverpool Street","happy":2}}, sort_keys=True, indent=4))
#        parsed_json = json.loads(json.dumps({"report":{"line":"Circle Line","categories":["Line Disruptions" , "Minor Delays"],"other":"This is a test.","station_1":"Euston","station_2":"Liverpool Street","twitter":"neal_lathia","time_stamp":"2011-08-01 11:37:21","direction":"Northbound","satisfaction":250}}, sort_keys=True, indent=4))
#        parsed_json = json.loads(json.dumps({"user":{"twitter":"neal_lathia"}}, sort_keys=True, indent = 4))
#        parsed_json = json.loads(json.dumps({"user":{"facebook":"599720869","given_name":"Bob","surname":"Bloggs","gender":"male","email":"joe.bloggs@internet.com"}}))
#        logging.info(self.request.body)
        parsed_json = json.loads(self.request.body) 

        self.process(parsed_json)
        self.response.out.write("<p>Processing complete</p></body></html>")
    
    def process(self, parsed_json):
        "determines how the parsed json should be processed and begins doing so"
        keys =  parsed_json.keys()
        for header in keys:
            if (header == 'check_in'):
                self.processing(header, parsed_json, True)
            if (header == 'report'):
                logging.info(header)
                self.processing(header, parsed_json, False)
            if (header == 'user'):
                self.process_user_request(header, parsed_json[header])
                
    def processing(self, header, parsed_json, is_check_in):
        "processing tasks common to both check-in and reports"
        user_id = self.find_user_Id(parsed_json[header].get('twitter'), parsed_json[header].get('facebook'))
        entry = parsed_json[header]
        time_stamp = datetime.strptime(entry.get('time_stamp'), '%Y-%m-%d %H:%M:%S')
        self.response.out.write("<p> time_stamp: " + str(time_stamp) + "</p>")
        
        if (self.is_not_in_database(user_id, time_stamp, is_check_in)):
            if (is_check_in):
                add_to_check_in_db(self, user_id, entry)
            else:
                add_to_reports_db(self, user_id, entry)
            self.response.out.write('<p>Added to the Database</p>')
        else:
            self.response.out.write('<p>Entry already exists')
            
    def process_user_request(self, header, user):
        "deals with either adding or updating user information"
        twitter_id = user.get('twitter')
        facebook_id = user.get('facebook')
        
        if ((twitter_id is not None) and (facebook_id is None) and (self.is_user_not_in_database(twitter_id, None, True) is None)):
            add_to_user_db(self, user)
            self.response.out.write("<p> Twitter user <i>" + twitter_id + "</i> added successfully</p>")
            
        elif ((twitter_id is None) and (facebook_id is not None) and (self.is_user_not_in_database(None, facebook_id, True) is None)):
            add_to_user_db(self, user)
            self.response.out.write("<p> Facebook user <i>" + facebook_id + "</i> added successfully</p>")
            
        elif ((twitter_id is not None) and (facebook_id is not None)):
            state = self.is_user_not_in_database(twitter_id, facebook_id, True)
            
            if (state is None):
                self.response.out.write("<p>Adding new user with Twitter and Facebook credentials to database<p>")
                add_to_user_db(self, user)
                
            elif (len(state) == 1):
                self.response.out.write("<p> Twitter user: <i>" + twitter_id + "</i> and Facebook id: <i>" + facebook_id + "</i> credentials updated</p>")
                update_user_in_db(self, state[0], user)
                
            elif (len(state) == 2):
                self.response.out.write("<p> User already exists in Database </p>")
        else:
            self.response.out.write("<p> User already exists in Database </p>")
                
    def find_user_Id(self, twitter_id, facebook_id):
        "searches memcache for internal user id, otherwise searches database"
        self.response.out.write("<p>twitter: <i>" + str(twitter_id) + "</i> facebook: <i>" + str(facebook_id) + "</i></p>" )
        user = self.is_user_not_in_database(twitter_id, facebook_id, False)
        logging.info(user)
        returning_key = user[0]
        return returning_key
    
    def is_not_in_database(self, user_id, time_stamp, is_check_in):
        "searches database/memcache to check that the prospective entry has not already been entered"
        if (is_check_in):
            return self.query_check_in_db(user_id, time_stamp)
        else:
            logging.info('is_check_in: ' + str(is_check_in))
            return self.query_report_db(user_id, time_stamp)
        
    def is_user_not_in_database(self, twitter_id, facebook_id, addition):
        "checks to see if the twitter login is not in the database"
        logging.info('twitter_id: ' + str(twitter_id))
        logging.info('addition: ' + str(addition))
        to_return = None
        if (twitter_id is not None):
            if not addition:
                logging.info("accessing the memcache")
                t_entry = self.check_memcache(twitter_id, True)
                logging.info('t_entry: ' + str(t_entry))
            else:
                logging.info('bypassing the memcache')
                t_entry = self.check_twitter_user(twitter_id)
            if t_entry is not None:
                if (len(t_entry) > 0):
                    to_return = [t_entry[0]]
                
        if (facebook_id is not None):
            f_entry = self.check_memcache(facebook_id, False)
            if (len(f_entry) > 0):
                if (to_return is None):
                    to_return = [f_entry[0]]
                else:
                    to_return.append(f_entry[0])
                    
        return to_return
    
    def check_memcache(self, user_id, twitter):
        "checks memcache for user before consulting database"
        logging.info('twitter: ' + str(twitter))
        logging.info('user_id: ' + str(user_id))
        cache = memcache.Client()
        entry = cache.get(user_id)
        
        if entry is not None:
            logging.info('entry is not None')
            if len(entry) > 0:
                logging.info('len(entry) = ' + str(len(entry)))
                logging.info('entry: ' + str(entry))
                return entry
        
        else:
            if twitter:
                logging.info('checking twitter user from database')
                entry = self.check_twitter_user(user_id)
            else:
                entry = self.check_facebook_user(user_id)
                logging.info('~~~check_memcache: ' + str(entry))
                
            cache.add(user_id, entry, 0, 60)
            self.response.out.write("<p><i>from database</i></p>")
            return entry
        
    def check_twitter_user(self, twitter_id):
        logging.info('twitter_id: ' + str(twitter_id))
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
        fetched = query.fetch(1) 
        logging.info('~~~check_facebook_user: ' + facebook_id + ', 599720869')
        return fetched
            
    def query_check_in_db(self, user_id, time_stamp):
        "commences the Check-In database search"
        query = db.GqlQuery("SELECT __key__ "
                            "FROM check_in_db "
                            "WHERE ANCESTOR IS :1 AND time_sent = :2 AND user = :3",
                            check_in_db_key('check_in_database'),
                            time_stamp,
                            user_id
                            )
        entry = query.fetch(1)
        if (len(entry) > 0):
            return False
        else:
            return True
        
    def query_report_db(self, user_id, time_stamp):
        "commences the Report database search"
        query = db.GqlQuery("SELECT __key__ "
                            "FROM report_db "
                            "WHERE ANCESTOR IS :1 AND time_sent = :2 AND user = :3",
                            report_db_key('report_database'),
                            time_stamp,
                            user_id
                            )
        entry = query.fetch(1)
        if (len(entry) > 0):
            logging.info('returning false')
            return False
        else:
            logging.info('returning true')
            return True

def main():
    application = webapp.WSGIApplication([('/upload/post', get_raw)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()