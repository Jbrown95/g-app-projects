import re
import time
import hmac
from models import users
from handlers import handler
from google.appengine.ext import db
from handlers import handler
SECRET = "thisissupersupersecret"


User = users.User
Handler = handler.Handler

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

def hash_str(string):
    """hashes usernames for use in cookies"""
    return hmac.new(SECRET, string).hexdigest()

def make_secure_val(string):
    """used to create the hash used in cookies"""
    return "%s|%s" % (string, hash_str(string))

def check_secure_val(string):
    """used for checking cookies to validate current user"""
    if string:
        val = string.split('|')[0]
        if string == make_secure_val(val):
            return val

def valid_username(username):
    """validates usernames"""
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")

def valid_password(password):
    """validates passwords"""
    return PASS_RE.match(password)


Handler = handler.Handler
class LoginPage(Handler):
    """loging class"""
    def get(self):
        """gets login form"""
        self.render('login.html')

    def post(self):
        """submits loging form"""
        username = self.request.get("username")
        password = self.request.get("password")

        qs1 = "Select * from User where user = '{}'".format(username)
        qry1 = db.GqlQuery(qs1)
        try:
            user_query = qry1[0].user
            pw_query = qry1[0].password
        except BaseException:
            user_query = None
            pw_query = None

        if username == user_query and hash_str(password) == pw_query:
            self.redirect("welcome")
            username_cookie = make_secure_val(str(username))
            self.response.headers.add_header('Set-Cookie', 'username=%s' % username_cookie)
        elif username == user_query and not password == pw_query:
            self.render('login.html', error_password='incorrect password', username=username)
        elif not username == user_query and password == pw_query:
            self.render('login.html', error_username='no username')
        else:
            self.render('login.html', error_username='no username')
