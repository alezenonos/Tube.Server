from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson as json
from test_uploader.receive_check_ins import add_to_check_in_db
from test_uploader.receive_reports import add_to_reports_db
from test_uploader.receive_user import add_to_user_db
from test_uploader.receive_user import update_user_in_db
from data.check_in_db import check_in_db_key
from data.report_db import report_db_key
from data.user_db import user_db_key
from datetime import datetime

class get_raw(webapp.RequestHandler):
    "gets the raw submitted data from the client"
    def post(self):
#    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write('<html><body>')
#        parsed_json = json.loads(json.dumps({"check_in":{"time_stamp":"2987-07-31 08:25:10","delay":2,"facebook":"testfb","message":"","crowd":2,"latitude":"51.5315581","longitude":"-0.13440335","origin":"Euston","modality":"tube","destination":"Liverpool Street","happy":2}}, sort_keys=True, indent=4))
#        parsed_json = json.loads(json.dumps({"report":{"line":"Circle Line","categories":["Line Disruptions" , "Minor Delays"],"comment":" ","stations":["Barbican"],"twitter":"alezenonos01","time_stamp":"2011-08-01 11:37:18"}}, sort_keys=True, indent=4))
#        parsed_json = json.loads(json.dumps({"user":{"twitter":"alezenonos01"}}, sort_keys=True, indent = 4))
#        parsed_json = json.loads(json.dumps({"user":{"facebook":"testfb","given_name":"Bob","surname":"Bloggs","gender":"male","email":"joe.bloggs@internet.com"}}))
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
                self.processing(header, parsed_json, False)
            if (header == 'user'):
                self.process_user_request(header, parsed_json[header])
                
    def processing(self, header, parsed_json, is_check_in):
        "processing tasks common to both check-in and reports"
        user_id = self.find_user_Id(parsed_json[header].get('twitter'), parsed_json[header].get('facebook'))
        entry = parsed_json[header]
        time_stamp = datetime.strptime(entry['time_stamp'], '%Y-%m-%d %H:%M:%S')
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
        if ((twitter_id != None) and (facebook_id == None) and (self.is_user_not_in_database(twitter_id, None) == None)):
            add_to_user_db(self, user)
            self.response.out.write("<p> Twitter user <i>" + twitter_id + "</i> added successfully</p>")
        elif ((twitter_id == None) and (facebook_id != None) and (self.is_user_not_in_database(None, facebook_id) == None)):
            add_to_user_db(self, user)
            self.response.out.write("<p> Facebook user <i>" + facebook_id + "</i> added successfully</p>")
        elif ((twitter_id != None) and (facebook_id != None)):
            state = self.is_user_not_in_database(twitter_id, facebook_id)
            if (state == None):
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
        user = self.is_user_not_in_database(twitter_id, facebook_id)
        returning_key = user[0].key()
        return returning_key
    
    def is_not_in_database(self, user_id, time_stamp, is_check_in):
        "searches database/memcache to check that the prospective entry has not already been entered"
        if (is_check_in):
            return self.query_check_in_db(user_id, time_stamp)
        else:
            return self.query_report_db(user_id, time_stamp)
        
    def is_user_not_in_database(self, twitter_id, facebook_id):
        "checks to see if the twitter login is not in the database"
        to_return = None
        if (twitter_id != None):
            t_entry = self.check_twitter_user(twitter_id)
            if (len(t_entry) > 0):
                to_return = [t_entry[0]]
        if (facebook_id != None):
            f_entry = self.check_facebook_user(facebook_id)
            if (len(f_entry) > 0):
                if (to_return == None):
                    to_return = [f_entry[0]]
                else:
                    to_return.append(f_entry[0])
        return to_return
        
    def check_twitter_user(self, twitter_id):
        query = db.GqlQuery(
                            "SELECT * "
                            "FROM user_db "
                            "WHERE ANCESTOR IS :1 AND twitter_id = :2",
                            user_db_key('user_database'),
                            twitter_id
                            )
        return query.fetch(1)
    
    def check_facebook_user(self, facebook_id):
        query = db.GqlQuery(
                            "SELECT * "
                            "FROM user_db "
                            "WHERE ANCESTOR IS :1 AND facebook_id = :2",
                            user_db_key('user_database'),
                            facebook_id
                            )
        return query.fetch(1)
            
    def query_check_in_db(self, user_id, time_stamp):
        "commences the Check-In database search"
        query = db.GqlQuery("SELECT * "
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
        query = db.GqlQuery("SELECT * "
                            "FROM report_db "
                            "WHERE ANCESTOR IS :1 AND time_sent = :2 AND user = :3",
                            report_db_key('report_database'),
                            time_stamp,
                            user_id
                            )
        entry = query.fetch(1)
        if (len(entry) > 0):
            return False
        else:
            return True

def main():
    application = webapp.WSGIApplication([('/upload/post', get_raw)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()