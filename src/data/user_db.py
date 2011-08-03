from google.appengine.ext import db

class user_db(db.Model):
    given_name = db.StringProperty()
    surname = db.StringProperty()
    gender = db.StringProperty()
    email = db.StringProperty() # Conversion to EmailProperty?
    twitter_id = db.StringProperty()
    facebook_id = db.StringProperty()
    log_file = db.StringProperty()
    
def user_db_key(user_db_name=None):
    return db.Key.from_path('user_db', user_db_name or 'user_database')