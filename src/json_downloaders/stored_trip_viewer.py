from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from data.distance_db import Trip

class main_page(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        for i in range(0,9):
            query = Trip.all()
            query = db.GqlQuery(
                                "SELECT * "
                                "FROM Rating "
                                "WHERE Origin = :1 AND Destination = :2 ",
                                "Archway",
                                "Goodge Street"
                                )
            entries = query.fetch(100)
            for entry in entries:
                self.response.out.write("<p>Origin: </i>" + entry.Origin + "</i></p>")
                self.response.out.write("<p>Destination: </i>" + entry.Destination + "</i></p>")
#                self.response.out.write("<p>Miles: </i>" + entry.Miles + "</i></p>")
#                self.response.out.write("<p>Points: </i>" + entry.Points + "</i></p>")
#                self.response.out.write("<p>Popularity: </i>" + entry.Popularity + "</i></p><hr>")
            
            self.response.out.write("<hr><hr><br><p>~END OF QUERY~</p>")
            
class Trip(db.Model):
    Origin = db.StringProperty()
    Destination = db.StringProperty()
    Miles = db.StringProperty()
    Points = db.StringProperty()
    Popularity = db.StringProperty()
    
class Rating(db.Model):
    destination = db.StringProperty()
    modality = db.StringProperty()
    origin = db.StringProperty()
    rating = db.IntegerProperty()
    rating_time = db.StringProperty()
    received_time = db.IntegerProperty()
    submit_location = db.StringProperty()
    user = db.StringProperty()
            

application = webapp.WSGIApplication([('/get/distances', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()