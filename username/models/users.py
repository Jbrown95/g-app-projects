from google.appengine.ext import db
class User(db.Model):
    """user library"""
    user = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
