from models import blogpost
from handlers import handler
from google.appengine.ext import db
import time
"""models"""
BlogPost = blogpost.BlogPost
"""handlers"""
Handler = handler.Handler
class Edit(Handler):
    """edit post class"""
    def get(self, post_id):
        """gets the post to edit"""
        blogpost_key = db.Key.from_path('BlogPost', int(post_id))
        blogpost_post = db.get(blogpost_key)
        content = blogpost_post.content
        title = blogpost_post.title
        self.render('edit.html', title=title, content=content)
    def post(self, post_id):
        """Method for editing posts"""
        blogpost_key = db.Key.from_path('BlogPost', int(post_id))
        blogpost_post = db.get(blogpost_key)
        content = self.request.get('content')
        title = self.request.get('title')
        blogpost_post.content = content
        blogpost_post.title = title
        blogpost_post.put()
        time.sleep(1)
        self.redirect('/permalink/{}'.format(str(post_id)))
