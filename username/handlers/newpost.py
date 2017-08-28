from models import likes
from models import blogpost
from handlers import handler
import time
"""handler"""
Handler = handler.Handler

"""models"""
Likes = likes.Likes
BlogPost = blogpost.BlogPost

class NewPost(Handler):
    """Newpost class"""
    def get(self):
        """method that gets the newpost forms"""
        self.render('newpost.html')
    def post(self):
        """method that creates a new post"""
        title = self.request.get("title")
        content = self.request.get("content")
        user = self.request.cookies.get('username').split('|')[0]

        if title and content:
            newpost = BlogPost(title=title, content=content, user=user)
            newpost.put()
            like = Likes(post=str(newpost.key().id()))
            like.put()

            newpost_url = ('/permalink/{}'.format(str(newpost.key().id())))
            time.sleep(1)
            self.redirect(newpost_url)
        else:
            error = "Double check and make sure you have a title and artwork."
            self.render("newpost.html", error=error, title=title, content=content)
