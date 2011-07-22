from google.appengine.ext import db

# database entity for check-ins
class check_in_db(db.Model):
    user = db.ReferenceProperty()
    origin = db.IntegerProperty(required=True)
    destination = db.IntegerProperty(required=True)
    line = db.IntegerProperty()
    time_sent = db.DateTimeProperty(required=True)
    time_received = db.DateTimeProperty(required=True, auto_now_add=True)
    rating_delay = db.RatingProperty(required=True)
    rating_crowded = db.RatingProperty(required=True)
    comment = db.TextProperty(required=False)
    
# database entity for temporarty test of check-ins (to be removed)
#class check_in_test(db.Model):
#    date = db.DateTimeProperty(auto_now_add=True)
#    comment = db.TextProperty(required=True)
    
# specifies that the entities are to be stored in the high replication datastore, and its key
def check_in_db_key(check_in_name=None):
    return db.Key.from_path('check_in_db', check_in_name or 'check_in_database')

    

    