from google.appengine.ext import db

# database entity for check-ins
class check_in_db(db.Model):
#    user needs to be a ref. to the other database
    user = db.StringProperty()
    origin = db.StringProperty(required=True)
    destination = db.StringProperty(required=True)
    line = db.StringListProperty()
    time_sent = db.DateTimeProperty(required=True)
    time_received = db.DateTimeProperty(required=True, auto_now_add=True)
    rating_delay = db.IntegerProperty(required=True)
    rating_crowded = db.IntegerProperty(required=True)
    rating_happiness = db.IntegerProperty(required=True)
    longitude = db.StringProperty(required=True)
    latitude = db.StringProperty(required=True)
    comment = db.TextProperty(required=False)
    
    
def check_in_db_key(check_in_name=None):
    return db.Key.from_path('check_in_db', check_in_name or 'check_in_database')

    

    