from models import likes
from handlers import handler
from google.appengine.ext import db
import time
"""models"""
Likes = likes.Likes
"""handlers"""
Handler = handler.Handler

SECRET = "thisissupersupersecret"

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

class Like(Handler):
    """Class is called to run the method below"""
    def get(self, post_id):
        """This is the method that is called when someone likes a post"""
        user_name_cookie = self.request.cookies.get('username')
        user = check_secure_val(user_name_cookie)
        if check_secure_val(user_name_cookie):
            like_index = Likes.all().filter('post =', post_id).filter('user =', user)
            try:
                current_user = like_index[0].user
            except BaseException:
                current_user = None
            if current_user == user:
                pass
            else:
                like = Likes(post=post_id, user=user)
                like.put()
        time.sleep(1)
        self.redirect('/permalink/{}'.format(str(post_id)))
