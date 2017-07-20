import os
import jinja2
import webapp2
import re


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")

def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_email(email):
    return EMAIL_RE.match(email)



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):


    def get(self):
        self.render("username.html",)
    def post(self):
        
        error_username=''
        v_username = ''
        username = self.request.get("username")
        if valid_username(username):
            v_username=username
        else:
            error_username="Invalid username"

        error_password = ''
        v_password = ''
        password = self.request.get("password")
        if valid_password(password):
            v_password=password
        else:
            error_password="invalid password"

        error_mismatch = ''
        v_verify = ''
        verify = self.request.get("verify")
        if verify == v_password:
            v_verify=verify
        else:
            error_mismatch = "Passwords do not match"

        error_email = ''
        v_email = ''
        email = self.request.get("email")
        if valid_email(email) or email == '':
            v_email=email
        else:
            error_email = "Invalid email"

        if v_username == username and not v_password == '' and v_verify == password and v_email == email:
            self.redirect('/welcome?username=' + v_username)
        else:
            self.render("username.html", username = v_username,
                                        password = v_password,
                                        verify = v_verify,
                                        email = v_email,
                                        error_username = error_username,
                                        error_password = error_password,
                                        error_mismatch = error_mismatch,
                                        error_email = error_email)




class WelcomePage(Handler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            self.render("welcome.html", username = username)
        else:
            self.redirect('/')




app = webapp2.WSGIApplication([('/', MainPage),
                                ('/welcome', WelcomePage)
                                ],
                                debug=True)
