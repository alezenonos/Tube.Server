from data.check_in_db import check_in_db
from data.check_in_db import check_in_db_key
from data.strings import tube_line_arrays
from data.strings import tube_lines
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import datetime
import logging

class get_raw(webapp.RequestHandler):
    "gets the raw submitted data from the client"
#    def get(self):
    def post(self):
        self.response.headers['Content-Type'] = "text/plain"
        
#        json_tester = json.dumps({"Checkin":{"time_stamp":"2011-07-28 08:24:15","delay":2,"user":"new test","message":"","crowd":2,"latitude":"51.5315581","longitude":"-0.13440335","origin":"Euston","modality":"tube","destination":"Liverpool Street","happy":2}}, sort_keys=True, indent=4)
        json_tester = self.request.body

        loaded_json = json.loads(json_tester)                
        processing().process_check_ins(loaded_json)
        
class processing():
    "processes the data and places it into the database"
    def process_check_ins(self, raw):
        "processes the check-ins obtained"
        for check_in in raw:
            self.add_to_db(raw[check_in])
    
    def add_to_db(self, check_in):
        "retreives the stored information and places it in the database"
        logging.info('add_to_db')
        logging.info(check_in)
        logging.info(check_in['modality'])
        if check_in['modality'] == 'tube':
            u=check_in['user']
            o=check_in['origin']
            d=check_in['destination']
            t=check_in['time_stamp']
    #        l=self.get_lines(check_in['line'])
            rd=check_in['delay']
            rc=check_in['crowd']
            rh=check_in['happy']
            longi=check_in['longitude']
            lat=check_in['latitude']
            c=check_in['message']
            
            t = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
#            This will need to be gotten rid of, but at the moment lines aren't sent so for other functionality this will have to do
            l = self.find_line(o) + self.find_line(d)
            
            key = check_in_db_key('check_in_database')
            entry = check_in_db(
                                parent = key,
                                user = u,
                                origin = o,
                                destination = d,
                                line = l,
                                time_sent = t,
                                rating_delay = rd,
                                rating_crowded = rc,
                                rating_happiness = rh,
                                longitude = longi,
                                latitude = lat,
                                comment = c
                                )
            entry.put()
    
    def get_lines(self, lines):
        "returns the lines in a recognisable format"
        returned = []
        for line in lines:
            returned.append(line)
        return returned
    
    def find_line(self, queried):
        "Depreciated (but necessary until lines are sent) - Called to find on which line the stations fall"
        returned = list()
        for line_id in range(len(tube_line_arrays)):
            for station in tube_line_arrays[line_id]:
                if station==queried:
                    returned.append(tube_lines[line_id])
        return returned
    
def main():
    application = webapp.WSGIApplication([('/posted/there', get_raw)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()