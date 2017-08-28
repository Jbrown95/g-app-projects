import time
from models import users
from models import blogpost
from models import comments
from handlers import handler
from google.appengine.ext import db
"""handlers"""
Handler = handler.Handler
"""models"""
User = users.User
BlogPost = blogpost.BlogPost

class WelcomePage(Handler):
    """class for welcome page"""
    def get(self):
        """get method for displaying welome page"""
        username = self.request.cookies.get('username')

        if username:
            username = username.split('|')[0]

        if username:
            time.sleep(1)
            users = db.GqlQuery('Select * from User')

            posts = BlogPost.all()
            posts.order('-created')

            self.render("welcome.html", users=users, username=username,
                        posts=posts)
        else:
            self.redirect('/')
