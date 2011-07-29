from data.user_db import user_db
from data.user_db import user_db_key
import logging

def add_to_user_db(self, user):
    logging.info('add_to_user_db')
    cn = user.get('given_name')
    sn = user.get('surname')
    g = user.get('gender')
    e = user.get('email')
    t = user.get('twitter')
    f = user.get('facebook')
    
    key = user_db_key('user_database')
    entry = user = user_db(
                           parent = key,
                           twitter_id = t,
                           facebook_id = f,
                           given_name = cn,
                           surname = sn,
                           gender = g,
                           email = e,
                           )
    entry.put()
    
def update_user_in_db(self, user_id, user):
    "Updates the given user in the database"
    self.response.out.write("<p> User_id: <i>" + user_id.key() + "</i></p>")
    entity = user_id
    entity.given_name = user.get('given_name')
    entity.surname = user.get('surname')
    entity.gender = user.get('gender')
    entity.email = user.get('email')
    entity.twitter_id = user.get('twitter')
    entity.facebook_id = user.get('facebook')
    entity.put()