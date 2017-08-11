import os
import jinja2
import webapp2
import re
import hmac
import time

from google.appengine.ext import db

SECRET = "thisissupersupersecret"

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    if h:
        val = h.split('|')[0]
        if h == make_secure_val(val):
            return val

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

COOKIE_RE = re.compile(r'.+=;\s*Path=/')
def valid_cookie(cookie):
    return cookie and COOKIE_RE.match(cookie)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


def user_key(name = 'default'):
    return db.Key.from_path('users', name)

class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    user = db.TextProperty(required = False)
    comments = db.StringProperty(required = False)


class User(db.Model):
    user = db.StringProperty(required = True)
    pw = db.StringProperty(required = True)


class MainPage(Handler):
    def get(self):
        self.redirect('/signup')

class SignUp(Handler):
    def get(self):
        users = db.GqlQuery('Select * from User')
        self.render("username.html")
    def post(self):
        error_username=''
        v_username = ''
        username = self.request.get("username")
        username_cookie_used = self.request.cookies.get('username')

        qs = "Select * from User where user = '{}'".format(username)
        qry = db.GqlQuery(qs)
        try:
            q = qry[0].user
        except:
            q = None

        if username == q:
            error_username="This username is already taken"
        elif valid_username(username):
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
            u = User(user = v_username, pw = v_password)
            u.put()

            username_cookie = make_secure_val(str(username))
            self.response.headers.add_header('Set-Cookie', 'username=%s' % username_cookie)

            self.redirect('/welcome')

        else:


            self.render("username.html", username=v_username,
                                        password=v_password,
                                        verify =v_verify,
                                        email =v_email,
                                        error_username = error_username,
                                        error_password = error_password,
                                        error_mismatch = error_mismatch,
                                        error_email = error_email)






class WelcomePage(Handler):


    def get(self):
        username = self.request.cookies.get('username')

        if username:
            username = username.split('|')[0]

        if username:
            time.sleep(1)
            users = db.GqlQuery('Select * from User')
            # posts = db.GqlQuery("SELECT * FROM BlogPost "
            #                     "ORDER BY created DESC")
            posts = BlogPost.all()
            posts.order('-created')

            self.render("welcome.html", users = users,username = username,posts = posts)
        else:
            self.redirect('/')

    #def render_front(self, title='', content='', error='',):





class LoginPage(Handler):
    def get(self):
            self.render('login.html')



    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        qs1 = "Select * from User where user = '{}'".format(username)
        qry1 = db.GqlQuery(qs1)
        try:
            q1 = qry1[0].user
            q2 = qry1[0].pw
        except:
            q1 = None
            q2 = None

        if username == q1 and password == q2:
            self.redirect("welcome")
            username_cookie = make_secure_val(str(username))
            self.response.headers.add_header('Set-Cookie', 'username=%s' % username_cookie)
        elif username == q1 and not password == q2:
            self.render('login.html', error_password = 'incorrect password', username = username)
        elif not username == q1 and password == q2:
            self.render('login.html', error_username = 'no username')
        else:
            self.render('login.html', error_username = 'no username')


class LogoutPage(Handler):
    def get(self):
        none = ''
        self.response.headers.add_header('Set-Cookie', 'username=; Path =/')
        self.redirect('/login')

class NewPost(Handler):
    def get(self):
        self.render('newpost.html')
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        user = self.request.cookies.get('username').split('|')[0]

        if title and content:
            a = BlogPost(title = title, content = content, user = user)
            a.put()
            newpost_url = ('/permalink/{}'.format(str(a.key().id())))
            time.sleep(1)
            self.redirect(newpost_url)
        else:
            error = "Double check and make sure you have a title and artwork."
            self.render("newpost.html", error = error,title = title, content = content)

class PostPage(Handler):
    def get(self,post_id):

        key = db.Key.from_path('BlogPost', int(post_id))
        post = db.get(key)
        content = post.content
        title = post.title
        user = post.user
        comments = post.comments
        current_user = self.request.cookies.get('username').split('|')[0]
        admin = "Joshua"
        if not post:
            self.error(404)
            return

        self.render("permalink.html",post = post,admin = admin, title = title, content = content, user = user, comments = comments, current_user = current_user)

    def post(self,post_id):
        comments = []
        comments.append(str(self.request.get('comments')))
        self.render("permalink.html", comments = comments)
        key = db.Key.from_path('BlogPost', int(post_id))
        post = db.get(key)
        for comment in comments:
            post.comments = comments
            post.put()
        self.redirect('/permalink/{}'.format(str(post_id)))
class Delete(Handler):
    def get(self,post_id):
        self.render('delete.html')
        h = self.request.cookies.get('username')
        if check_secure_val(h):
            key = db.Key.from_path('BlogPost', int(post_id))
            post = db.get(key)
            if post.user == h.split('|')[0] or h.split('|')[0] == "Joshua" :
                post.delete()
                self.redirect('/welcome')
            else:
                self.redirect('/welcome')
        else:
            self.redirect('/welcome')





app = webapp2.WSGIApplication([('/signup', SignUp),
                                ('/welcome', WelcomePage),
                                ('/', MainPage),
                                ('/login', LoginPage),
                                ('/logout', LogoutPage),
                                ('/newpost', NewPost),
                                ('/delete/([0-9]+)', Delete),
                                ('/permalink/([0-9]+)',PostPage)
                                ],
                                debug=True)
