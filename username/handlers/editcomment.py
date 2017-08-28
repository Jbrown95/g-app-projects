from models import comments
from handlers import handler
from google.appengine.ext import db
import time
"""models"""
Comments = comments.Comments
"""handlers"""
Handler = handler.Handler
class EditComment(Handler):
    """The Class for editing comments"""
    def get(self, post_id):
        """this is the get method to display the comment to be edited"""
        comments_key = db.Key.from_path('Comments', int(post_id))
        comments_post = db.get(comments_key)
        comment = comments_post.comment
        user = comments_post.user
        self.render('edit.html', user=user, comment=comment)
    def post(self, post_id):
        """this is the post method to edit a comment"""
        comments_key = db.Key.from_path('Comments', int(post_id))
        comments_post = db.get(comments_key)
        comment = self.request.get('comment')
        comments_post.comment = comment
        comments_post.user = comments_post.user
        comments_post.post = comments_post.post
        comments_post.put()
        time.sleep(1)
        self.redirect('/permalink/{}'.format(str(comments_post.post)))
