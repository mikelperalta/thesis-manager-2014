import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_GUESTBOOK_NAME1 = 'default_guestbook1'
DEFAULT_GUESTBOOK_NAME2 = 'default_guestbook2'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MemberOnePage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('MemberOnePage.html')
        self.response.write(template.render(template_values))

class MemberTwoPage(webapp2.RequestHandler):
   
    def get(self):
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('MemberTwoPage.html')
        self.response.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class Guestbook1(webapp2.RequestHandler):          
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.s
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/1?' + urllib.urlencode(query_params))

class Guestbook2(webapp2.RequestHandler):    
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.s
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/2?' + urllib.urlencode(query_params))

class HomePageHandler(webapp2.RequestHandler):          
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render())

class Adviser(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    department = ndb.StringProperty(indexed=False)
    title = ndb.StringProperty(indexed=False)
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    phone = ndb.StringProperty(indexed=False)

class AdviserNewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('adviser_new.html')
        self.response.write(template.render())

    def post(self):
        adviser = Adviser()
        adviser.department = self.request.get('department')
        adviser.title = self.request.get('title')
        adviser.first_name = self.request.get('first_name')
        adviser.last_name = self.request.get('last_name')
        adviser.email = self.request.get('email')
        adviser.phone = self.request.get('phone')
        adviser.put()
        self.redirect('/adviser/success')

class AdviserSuccessPageHandler(webapp2.RequestHandler):          
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('adviser_success.html')
        self.response.write(template.render())

class AdviserListHandler(webapp2.RequestHandler):          
    def get(self):
        adviser = Adviser.query().fetch()
        template_values = {
            'all_adviser' : adviser
        }

        template = JINJA_ENVIRONMENT.get_template('adviser_list.html')
        self.response.write(template.render(template_values))

class AdviserViewHandler(webapp2.RequestHandler):          
    def get(self, adviser_id):
        all_adviser = Adviser.query().fetch()
        adviser_id = int(adviser_id)

        values = {
            'all_adviser' : all_adviser,
            'id' : adviser_id
        }

        template = JINJA_ENVIRONMENT.get_template('adviser_view.html')
        self.response.write(template.render(values))

class AdviserEditHandler(webapp2.RequestHandler):          
    def get(self, adviser_id):
        all_adviser = Adviser.query().fetch()
        adviser_id = int(adviser_id)

        values = {
            'all_adviser' : all_adviser,
            'id' : adviser_id
        }

        template = JINJA_ENVIRONMENT.get_template('adviser_edit.html')
        self.response.write(template.render(values))

    def post(self, adviser_id):
        adviser_id = int(adviser_id)
        adviser = Adviser.get_by_id(adviser_id)
        adviser.department = self.request.get('department')
        adviser.title = self.request.get('title')
        adviser.first_name = self.request.get('first_name')
        adviser.last_name = self.request.get('last_name')
        adviser.email = self.request.get('email')
        adviser.phone = self.request.get('phone')
        adviser.put()
        self.redirect('/adviser/success')

class Student(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    department = ndb.StringProperty(indexed=False)
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    number = ndb.StringProperty(indexed=False)
    remarks = ndb.StringProperty(indexed=False)
    
class StudentNewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('student_new.html')
        self.response.write(template.render())

    def post(self):
        student = Student()
        student.department = self.request.get('department')
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.email = self.request.get('email')
        student.number = self.request.get('number')
        student.remarks = self.request.get('remarks')
        student.put()
        self.redirect('/student/success')

class StudentSuccessPageHandler(webapp2.RequestHandler):          
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('student_success.html')
        self.response.write(template.render())

class StudentListHandler(webapp2.RequestHandler):          
    def get(self):
        student = Student.query().fetch()
        template_values = {
            'all_student' : student
        }

        template = JINJA_ENVIRONMENT.get_template('student_list.html')
        self.response.write(template.render(template_values))

class StudentViewHandler(webapp2.RequestHandler):          
    def get(self, student_id):
        all_student = Student.query().fetch()
        student_id = int(student_id)

        values = {
            'all_student' : all_student,
            'id' : student_id
        }

        template = JINJA_ENVIRONMENT.get_template('student_view.html')
        self.response.write(template.render(values))

class StudentEditHandler(webapp2.RequestHandler):          
    def get(self, student_id):
        all_student = Student.query().fetch()
        student_id = int(student_id)

        values = {
            'all_student' : all_student,
            'id' : student_id
        }

        template = JINJA_ENVIRONMENT.get_template('student_edit.html')
        self.response.write(template.render(values))
    
    def post(self, student_id):
        student_id = int(student_id)
        student = Student.get_by_id(student_id)
        student.department = self.request.get('department')
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.email = self.request.get('email')
        student.number = self.request.get('number')
        student.remarks = self.request.get('remarks')
        student.put()
        self.redirect('/student/success')

class Thesis(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    year = ndb.StringProperty(indexed=False)
    status = ndb.StringProperty(indexed=False)

class ThesisNewHandler(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'username': users.get_current_user(),
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('thesis_new.html')
        self.response.write(template.render())

    def post(self):
        thesis = Thesis()
        thesis.title = self.request.get('title')
        thesis.description = self.request.get('description')
        thesis.year = self.request.get('year')
        thesis.status = self.request.get('status')
        thesis.put()
        self.redirect('/thesis/success')

class ThesisSuccessPageHandler(webapp2.RequestHandler):          
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('thesis_success.html')
        self.response.write(template.render())

class ThesisListHandler(webapp2.RequestHandler):          
    def get(self):
        thesis = Thesis.query().fetch()
        template_values = {
            'all_thesis' : thesis
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_list.html')
        self.response.write(template.render(template_values))

class ThesisViewHandler(webapp2.RequestHandler):          
    def get(self, thesis_id):
        all_thesis = Thesis.query().fetch()
        thesis_id = int(thesis_id)

        values = {
            'all_thesis' : all_thesis,
            'id' : thesis_id
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_view.html')
        self.response.write(template.render(values))

class ThesisEditHandler(webapp2.RequestHandler):          
    def get(self, thesis_id):
        all_thesis = Thesis.query().fetch()
        thesis_id = int(thesis_id)

        values = {
            'all_thesis' : all_thesis,
            'id' : thesis_id
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_edit.html')
        self.response.write(template.render(values))

    def post(self, thesis_id):
        thesis_id = int(thesis_id)   
        thesis = Thesis.get_by_id(thesis_id)
        thesis.title = self.request.get('title')
        thesis.description = self.request.get('description')
        thesis.year = self.request.get('year')
        thesis.status = self.request.get('status')
        thesis.put()
        self.redirect('/thesis/success')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/home',HomePageHandler),
    ('/sign', Guestbook),
    ('/sign1', Guestbook1),
    ('/sign2', Guestbook2),
    ('/module-1/1', MemberOnePage),
    ('/module-1/2', MemberTwoPage),
    ('/adviser/new', AdviserNewHandler),
    ('/adviser/success', AdviserSuccessPageHandler),
    ('/adviser/list', AdviserListHandler),
    ('/adviser/view/(\d+)', AdviserViewHandler),
    ('/adviser/edit/(\d+)', AdviserEditHandler),
    ('/student/new', StudentNewHandler),
    ('/student/success', StudentSuccessPageHandler),
    ('/student/list', StudentListHandler),
    ('/student/view/(\d+)', StudentViewHandler),
    ('/student/edit/(\d+)', StudentEditHandler),
    ('/thesis/new', ThesisNewHandler),
    ('/thesis/success', ThesisSuccessPageHandler),
    ('/thesis/list', ThesisListHandler),
    ('/thesis/view/(\d+)', ThesisViewHandler),
    ('/thesis/edit/(\d+)', ThesisEditHandler),
], debug=True)  