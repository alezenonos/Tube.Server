from google.appengine.ext import db

class log_db(db.Model):
    user = db.ReferenceProperty(required=True)
    log_time_stamp = db.DateTimeProperty(required=True)
    activity_time_stamp = db.DateTimeProperty(required=True)
    tag = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    
def log_db_key(log_db_name=None):
    return db.Key.from_path('log_db', log_db_name or 'log_database')