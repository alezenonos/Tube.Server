from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson as json
from test_uploader.receive_check_ins import add_to_check_in_db
from data.check_in_db import check_in_db_key
from datetime import datetime

class get_raw(webapp.RequestHandler):
    "gets the raw submitted data from the client"
    def post(self):
#    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write('<html><body>')
#        parsed_json = json.loads(json.dumps({"check_in":{"time_stamp":"2999-07-31 08:25:10","delay":2,"user":"now test","message":"","crowd":2,"latitude":"51.5315581","longitude":"-0.13440335","origin":"Euston","modality":"tube","destination":"Liverpool Street","happy":2}}, sort_keys=True, indent=4))
        parsed_json = json.loads(self.request.body) 

        self.process(parsed_json)
        self.response.out.write("<p>Processing complete</p></body></html>")
    
    def process(self, parsed_json):
        "determines how the parsed json should be processed and begins doing so"
        keys =  parsed_json.keys()
        for header in keys:
            if (header == 'check_in'):
                self.process_check_in(header, parsed_json)
            if (header == 'report'):
                self.response.out.write(header)
            if (header == 'user'):
                self.response.out.write(header)
                
    def process_check_in(self, header, parsed_json):
        user_id = self.find_user_Id(parsed_json[header]['user'])
        entry = parsed_json[header]
        time_stamp = datetime.strptime(entry['time_stamp'], '%Y-%m-%d %H:%M:%S')
        self.response.out.write("<p> time_stamp: " + str(time_stamp) + "</p>")
        
        if (self.is_in_database(user_id, time_stamp, True)):
            add_to_check_in_db(self, user_id, entry)
            self.response.out.write('<p>Added to the Database</p>')
        else:
            self.response.out.write('<p>Entry already exists</p>')
                
    def find_user_Id(self, user):
        "Searches memcache for internal user id, otherwise searches database"
        self.response.out.write("<p>user: " + user + "</p>" )
        return user
    
    def is_in_database(self, user_id, time_stamp, is_check_in):
        "Searches database/memcache to check that the prospective entry has not already been entered"
        if (is_check_in):
            return self.query_check_in_db(user_id, time_stamp)
        else:
            return self.query_reports_db(user_id, time_stamp)
            
    def query_check_in_db(self, user_id, time_stamp):
        "Commences the Check-In database search"
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

def main():
    application = webapp.WSGIApplication([('/upload/post', get_raw)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()