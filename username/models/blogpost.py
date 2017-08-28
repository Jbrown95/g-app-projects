from google.appengine.ext import db
class BlogPost(db.Model):
    """blog library"""
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    likes = db.IntegerProperty(required=False)
    user = db.TextProperty(required=False)
