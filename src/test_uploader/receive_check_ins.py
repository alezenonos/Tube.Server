from data.check_in_db import check_in_db
from data.check_in_db import check_in_db_key
from data.strings import tube_line_arrays
from data.strings import tube_lines
from datetime import datetime
import logging

def add_to_check_in_db(self, user_id, check_in):
    "retreives the stored information and places it in the database"
    logging.info('add_to_db')
    logging.info(check_in)
    logging.info(check_in['modality'])
    if check_in['modality'] == 'tube':
        u=user_id
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
        l = find_line(self, o) + find_line(self, d)
        
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