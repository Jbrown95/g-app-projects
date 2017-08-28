from models import comments
from models import likes
from models import blogpost
from models import users
import re
import hmac
from handlers import handler
from google.appengine.ext import db
import time

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

"""handlers"""
Handler = handler.Handler

"""models"""
Likes = likes.Likes
Comments = comments.Comments
BlogPost = blogpost.BlogPost

class Delete(Handler):
    """Delete Class"""
    def get(self, post_id):
        """method for deleting posts"""
        self.render('delete.html')
        username_cookie = self.request.cookies.get('username')
        if check_secure_val(username_cookie):
            key = db.Key.from_path('BlogPost', int(post_id))
            post = db.get(key)
            comments = Comments.all()
            comments.filter('post =', post_id)
            likes = Likes.all().filter('post =', post_id)


            if (post.user == username_cookie.split('|')[0] or
                    username_cookie.split('|')[0] == "Joshua"):
                post.delete()
                for comment in comments:
                    comment.delete()
                for like in likes:
                    like.delete()
                self.redirect('/welcome')
            else:
                self.redirect('/welcome')
        else:
            self.redirect('/welcome')
