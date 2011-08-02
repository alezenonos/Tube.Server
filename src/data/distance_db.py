from google.appengine.ext import db

class Trip(db.Model):
    Origin = db.StringProperty()
    Destination = db.StringProperty()
    Miles = db.StringProperty()
    Points = db.StringProperty()
    Popularity = db.StringProperty()
    
def report_db_key(report_db_name=None):
    return db.Key.from_path('report_db', report_db_name or 'report_database')