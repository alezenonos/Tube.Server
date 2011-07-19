from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

class entity(db.Model):
    line = db.StringProperty(multiline=False)

class main_page(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""\n<html>\n<head>\n<p> Header here </p>\n</head>\n<body>""")
        entities = entity.all()
        for e in entities:
            self.response.out.write("\n <p> ")
            self.response.out.write(e.key().id())
            self.response.out.write(" </p>")
            self.response.out.write("\n <p> <i> ")
            self.response.out.write(e.line)
            self.response.out.write("</i> </p>")
        self.response.out.write(""" \n</body>\n</html>""")
test = entity()
test.line = "The best measure of a man's honesty isn't his income tax return. It's the zero adjust on his bathroom scale."
test.put()
test2 = entity() 
test2.line = "If we couldn't laugh, we would all go insane."
test2.put()

application = webapp.WSGIApplication([('/', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()