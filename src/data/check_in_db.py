from google.appengine.ext import db

# database entity for check-ins
class check_in_db(db.Model):
    user = db.StringProperty()
    origin = db.StringProperty(required=True)
    destination = db.StringProperty(required=True)
    line = db.StringProperty()
    time_sent = db.StringProperty(required=True)
    time_received = db.DateTimeProperty(required=True, auto_now_add=True)
    rating_delay = db.StringProperty(required=True)
    rating_crowded = db.StringProperty(required=True)
    rating_happiness = db.StringProperty(required=True)
    comment = db.TextProperty(required=False)
    
# database entity for temporarty test of check-ins (to be removed)
#class check_in_test(db.Model):
#    date = db.DateTimeProperty(auto_now_add=True)
#    comment = db.TextProperty(required=True)
    
# specifies that the entities are to be stored in the high replication datastore, and its key
def check_in_db_key(check_in_name=None):
    return db.Key.from_path('check_in_db', check_in_name or 'check_in_database')

    

    