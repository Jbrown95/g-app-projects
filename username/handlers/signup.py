import re
import time
import hmac
from models import users
from handlers import handler
from google.appengine.ext import db


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

class SignUp(Handler):
    """signup class"""
    def get(self):
        """this gets the form for new signups"""
        self.render("username.html")
    def post(self):
        """this is a method for new signups """
        error_username = ''
        error_password = ''
        error_mismatch = ''
        username = self.request.get("username")
        password = self.request.get('password')
        query_string = "Select * from User where user = '{}'".format(username)
        query = db.GqlQuery(query_string)
        try:
            old_user = query[0].user
        except BaseException:
            old_user = None


        if username != old_user and valid_username(username):
            if valid_password(password):
                if password == self.request.get('verify'):
                    User(user=username, password=hash_str(password)).put()

                    self.response.headers.add_header('Set-Cookie',
                    'username=%s' % make_secure_val(str(username)))

                    self.redirect('/welcome')
                else:
                    error_mismatch = "Passwords don't match."
                    self.render("username.html", username=username,
                                password=password,
                                error_mismatch=error_mismatch)

            else:
                error_password = "invalid password"
                self.render("username.html", username=username,
                            email=self.request.get('email'),
                            error_password=error_password)

        elif username == old_user:
            error_username = "This username is already taken"
            self.render("username.html", error_username=error_username)

        else:
            error_username = "Invalid username"
            if not valid_password(password):
                error_password = "Invalid Password"
                self.render("username.html", error_username=error_username,
                            error_password=error_password)

            elif password != self.request.get('verify'):
                error_mismatch = "passwords dont match"
                self.render("username.html",
                            error_username=error_username,
                            error_mismatch=error_mismatch)

            else:
                self.render("username.html",
                            error_username=error_username,
                            error_password=error_password,
                            error_mismatch=error_mismatch)
