from models import comments
from handlers import handler
from google.appengine.ext import db
import time
"""models"""
Comments = comments.Comments
"""handlers"""
Handler = handler.Handler
class DeleteComment(Handler):
    """Delete Comment class"""
    def get(self, post_id):
        """Delete comment method"""
        self.render('deletecomment.html')
        key = db.Key.from_path('Comments', int(post_id))
        post = db.get(key)
        url = post.post
        user_name_cookie = self.request.cookies.get('username')
        if check_secure_val(user_name_cookie):
            post.delete()
            time.sleep(1)
            self.redirect('/permalink/{}'.format(url))
