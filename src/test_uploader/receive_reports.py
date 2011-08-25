from data.report_db import report_db
from data.report_db import report_db_key
from datetime import datetime
import logging

def add_to_reports_db(self, user_id, report):
    logging.info('adding_to_reports_db')
    
    u = user_id
    ts = datetime.strptime(report.get('time_stamp'), '%Y-%m-%d %H:%M:%S')
    l = report.get('line')
    s1 = report.get('station_1')
    s2 = report.get('station_2')
    sat = report.get('satisfaction')
    direct = report.get('direction')
    oth = report.get('other')
    
    key = report_db_key('report_database')
    entry = report_db(
                      parent = key,
                      user = u,
                      time_sent = ts,
                      line = l,
                      station_1 = s1,
                      station_2 = s2,
                      direction = direct,
                      satisfaction_rating = sat,
                      other = oth
                      )
    
    dr = None
    cr = None
    complaints = []
    for complaint in report.get('categories'):
        if (complaint == 'Minor Delays'):
            dr = 350
        elif (complaint == 'Major Delays'):
            dr = 450
        elif (complaint == 'Crowded Train') or (complaint == 'Crowded') or (complaint == 'Crowded Platform'):
            cr = 350
        else:
            complaints.append(complaint)
    if dr is not None:
        entry.delay_rating = dr
    if cr is not None:
        entry.crowd_rating = cr
    entry.category = complaints
    
    entry.put()