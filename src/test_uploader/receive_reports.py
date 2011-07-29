from data.report_db import report_db
from data.report_db import report_db_key
from datetime import datetime
import logging

def add_to_reports_db(self, user_id, report):
    logging.info('adding_to_reports_db')
    
    u = user_id
    ts = datetime.strptime(report['time_stamp'], '%Y-%m-%d %H:%M:%S')
    l = report['line']
    s = report['stations']
    cat = report['categories']
    com = report['comment']
    
    key = report_db_key('report_database')
    entry = report_db(
                      parent = key,
                      user = u,
                      time_sent = ts,
                      line = l,
                      stations = s,
                      category = cat,
                      comment = com
                      )
    entry.put()