from models import comments
from models import likes
from models import blogpost
from handlers import handler
from google.appengine.ext import db
import time
"""handlers"""
Handler = handler.Handler

"""models"""
Likes = likes.Likes
Comments = comments.Comments
BlogPost = blogpost.BlogPost

class PostPage(Handler):
    """Class for permalink posts"""
    def get(self, post_id):
        """Get method for posts to be displayed at permalink"""
        blogpost_key = db.Key.from_path('BlogPost', int(post_id))
        blogpost_post = db.get(blogpost_key)
        content = blogpost_post.content
        title = blogpost_post.title
        post_user = blogpost_post.user
        like_qry_str = "Select * from Likes where post = '{}'".format(post_id)
        like_qry = db.GqlQuery(like_qry_str)
        likes = -1
        for item in like_qry:
            likes += 1
        comments = ''
        comments = Comments.all()
        comments.filter('post =', post_id).order('-created')

        current_user = self.request.cookies.get('username').split('|')[0]
        admin = "Joshua"
        if not blogpost_post:
            self.error(404)
            return
        self.render("permalink.html", post=blogpost_post, admin=admin,
                    title=title, content=content, post_user=post_user,
                    comments=comments, current_user=current_user, likes=likes)

    def post(self, post_id):
        """Comment post method"""
        username_cookie = self.request.cookies.get('username')
        if check_secure_val(username_cookie):
            user = username_cookie.split('|')[0]
        else:
            self.redirect('/permalink/{}'.format(str(post_id)))
        if self.request.get('comments') != '':
            comment = self.request.get('comments')
            cmt = Comments(comment=comment, user=user, post=post_id)
            cmt.put()
            time.sleep(1)
        self.redirect('/permalink/{}'.format(str(post_id)))
