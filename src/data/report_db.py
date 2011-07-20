from google.appengine.ext import db

class report_db(db.Model):
    user = db.ReferenceProperty()
    time_sent = db.DateTimeProperty(required=True)
    time_received = db.DateTimeProperty(required=True, auto_now_add=True)
    category = db.LinkProperty(float)
    comment = db.TextProperty(required=False)
    
#class report_db_test(db.Model):
#    date = db.DateTimeProperty(auto_now_add=True)
#    report = db.TextProperty(required=True)
    
def report_db_key(report_db_name=None):
    return db.Key.from_path('report_db', report_db_name or 'report_db_database')