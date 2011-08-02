
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import os

url_ci = '/check-in'
url_ci_lt = 'Check-ins'
url_r = '/reports'
url_r_lt = 'Reports'
url_u = '/users'
url_u_lt = 'Users'
url_f = '/get/fares'
fares_linktext = 'Fares'
url_ave = '/get/tube-lines-status'
ave_linktext = 'Tube lines status averages'
url_d = '/get/distances'
url_d_lt = 'Stations\' Distances'
    
class main_page(webapp.RequestHandler):
    def get(self):
        template_values = {
            'url_check_in' : url_ci,
            'url_check_in_linktext' : url_ci_lt,
            'url_report' : url_r,
            'url_report_linktext' : url_r_lt,
            'url_users' : url_u,
            'url_users_linktext' : url_u_lt,
            'url_fares' : url_f,
            'fares_linktext' : fares_linktext,
            'url_ave' : url_ave,
            'ave_linktext' : ave_linktext,
            'url_distances' : url_d,
            'url_distances_linktext' : url_d_lt
        }
        path = os.path.join(os.path.dirname(__file__), 'home.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', main_page)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()