from google.appengine.ext import db

class report_db(db.Model):
    user = db.ReferenceProperty(required=True)
    time_sent = db.DateTimeProperty(required=True)
    time_received = db.DateTimeProperty(required=True, auto_now_add=True)
    line = db.StringProperty(required=True)
    stations = db.StringListProperty(required=True)
    category = db.StringListProperty(required=True)
    comment = db.StringProperty(required=False)
    
def report_db_key(report_db_name=None):
    return db.Key.from_path('report_db', report_db_name or 'report_database')