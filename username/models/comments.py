from google.appengine.ext import db
class Comments(db.Model):
    """comments library"""
    comment = db.StringProperty(required=True)
    user = db.TextProperty(required=True)
    post = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
