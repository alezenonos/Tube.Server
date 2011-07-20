from google.appengine.ext import db

class user_db(db.Model):
    given_name = db.StringProperty()
    surname = db.StringProperty()
    login_twitter = db.StringProperty()
    login_facebook = db.StringProperty()
    login_google = db.StringProperty()
    
#class user_test(db.Model):
#    date = db.DateTimeProperty(auto_now_add=True)
#    name = db.TextProperty(required=True)
    
def user_db_key(user_db_name=None):
    return db.Key.from_path('user_db', user_db_name or 'user_database')