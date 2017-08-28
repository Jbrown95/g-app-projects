"""Main .py for blog site"""
import os
import time
import hmac
import re
import jinja2
import webapp2
from google.appengine.ext import db
"""import models"""
from models import users
from models import blogpost
from models import comments
from models import likes
"""import handlers"""
from handlers import signup
from handlers import mainpage
from handlers import welcomepage
from handlers import loginpage
from handlers import logoutpage
from handlers import newpost
from handlers import postpage
from handlers import delete
from handlers import deletecomment
from handlers import edit
from handlers import editcomment
from handlers import like




"""models"""
Likes = likes.Likes
Comments = comments.Comments
BlogPost = blogpost.BlogPost
User = users.User

"""handlers"""
SignUp = signup.SignUp
MainPage = mainpage.MainPage
WelcomePage = welcomepage.WelcomePage
LoginPage = loginpage.LoginPage
LogoutPage = logoutpage.LogoutPage
NewPost = newpost.NewPost
PostPage = postpage.PostPage
Delete = delete.Delete
DeleteComment = deletecomment.DeleteComment
Edit = edit.Edit
EditComment = editcomment.EditComment
Like = like.Like


# EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

# def valid_email(email):
    # return EMAIL_RE.match(email)

# def user_key(name='default'):
#     return db.Key.from_path('users', name)








app = webapp2.WSGIApplication([('/signup', SignUp),
                               ('/welcome', WelcomePage),
                               ('/', MainPage),
                               ('/login', LoginPage),
                               ('/logout', LogoutPage),
                               ('/newpost', NewPost),
                               ('/delete/([0-9]+)', Delete),
                               ('/permalink/([0-9]+)', PostPage),
                               ('/edit/([0-9]+)', Edit),
                               ('/editcomment/([0-9]+)', EditComment),
                               ('/like/([0-9]+)', Like),
                               ('/deletecomment/([0-9]+)', DeleteComment),
                              ], debug=True)
