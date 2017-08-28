from google.appengine.ext import db
class Likes(db.Model):
    """Post like library"""
    post = db.StringProperty(required=True)
    user = db.StringProperty(required=False)
