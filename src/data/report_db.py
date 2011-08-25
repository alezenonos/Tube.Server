from google.appengine.ext import db

class report_db(db.Model):
    user = db.ReferenceProperty(required=True)
    time_sent = db.DateTimeProperty(required=True)
    time_received = db.DateTimeProperty(required=True, auto_now_add=True)
    line = db.StringProperty()
    station_1 = db.StringProperty()
    station_2 = db.StringProperty()
    direction = db.StringProperty()
    satisfaction_rating = db.IntegerProperty(required=True)
    crowd_rating = db.IntegerProperty()
    delay_rating = db.IntegerProperty()
    category = db.StringListProperty()
    other = db.StringProperty()
    
def report_db_key(report_db_name=None):
    return db.Key.from_path('report_db', report_db_name or 'report_database')