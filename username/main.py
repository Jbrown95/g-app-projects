"""Main .py for blog site"""
import os
import time
import hmac
import re
import jinja2
import webapp2
from google.appengine.ext import db

SECRET = "thisissupersupersecret"

def hash_str(string):
    """hashes usernames for use in cookies"""
    return hmac.new(SECRET, string).hexdigest()

def make_secure_val(string):
    """used to create the hash used in cookies"""
    return "%s|%s" % (string, hash_str(string))

def check_secure_val(string):
    """used for checking cookies to validate current user"""
    if string:
        val = string.split('|')[0]
        if string == make_secure_val(val):
            return val

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

def valid_username(username):
    """validates usernames"""
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")

def valid_password(password):
    """validates passwords"""
    return PASS_RE.match(password)

# EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

# def valid_email(email):
    # return EMAIL_RE.match(email)



class Handler(webapp2.RequestHandler):
    """Parent Class for all pages that need to call templates"""
    def write(self, *a, **kw):
        """writes to page"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """allows jinja to render templates from /template"""
        temp = JINJA_ENV.get_template(template)
        return temp.render(params)

    def render(self, template, **kw):
        """renders templates using render_str"""
        self.write(self.render_str(template, **kw))


# def user_key(name='default'):
#     return db.Key.from_path('users', name)


class Likes(db.Model):
    """Post like library"""
    post = db.StringProperty(required=True)
    user = db.StringProperty(required=False)
class Comments(db.Model):
    """comments library"""
    comment = db.StringProperty(required=True)
    user = db.TextProperty(required=True)
    post = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class BlogPost(db.Model):
    """blog library"""
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    likes = db.IntegerProperty(required=False)
    user = db.TextProperty(required=False)


class User(db.Model):
    """user library"""
    user = db.StringProperty(required=True)
    password = db.StringProperty(required=True)


class MainPage(Handler):
    """redirects to login"""
    def get(self):
        """assumes no cookie, redirects to login"""
        self.redirect('/login')

class SignUp(Handler):
    """signup class"""
    def get(self):
        """this gets the form for new signups"""
        self.render("username.html")
    def post(self):
        """this is a method for new signups """
        error_username = ''
        error_password = ''
        error_mismatch = ''
        username = self.request.get("username")
        password = self.request.get('password')
        query_string = "Select * from User where user = '{}'".format(username)
        query = db.GqlQuery(query_string)
        try:
            old_user = query[0].user
        except BaseException:
            old_user = None


        if username != old_user and valid_username(username):
            if valid_password(password):
                if password == self.request.get('verify'):
                    User(user=username, password=hash_str(password)).put()

                    self.response.headers.add_header('Set-Cookie',
                    'username=%s' % make_secure_val(str(username)))

                    self.redirect('/welcome')
                else:
                    error_mismatch = "Passwords don't match."
                    self.render("username.html", username=username,
                                password=password,
                                error_mismatch=error_mismatch)

            else:
                error_password = "invalid password"
                self.render("username.html", username=username,
                            email=self.request.get('email'),
                            error_password=error_password)

        elif username == old_user:
            error_username = "This username is already taken"
            self.render("username.html", error_username=error_username)

        else:
            error_username = "Invalid username"
            if not valid_password(password):
                error_password = "Invalid Password"
                self.render("username.html", error_username=error_username,
                            error_password=error_password)

            elif password != self.request.get('verify'):
                error_mismatch = "passwords dont match"
                self.render("username.html",
                            error_username=error_username,
                            error_mismatch=error_mismatch)

            else:
                self.render("username.html",
                            error_username=error_username,
                            error_password=error_password,
                            error_mismatch=error_mismatch)

# ============
#         if username == old_user:
#             error_username = "This username is already taken"
#         elif valid_username(username):
#             v_username = username
#         else:
#             error_username = "Invalid username"
#
#         error_password = ''
#         v_password = ''
#         password = self.request.get("password")
#         if valid_password(password):
#             v_password = password
#         else:
#             error_password = "invalid password"
#
#         error_mismatch = ''
#         v_verify = ''
#         verify = self.request.get("verify")
#         if verify == v_password:
#             v_verify = verify
#         else:
#             error_mismatch = "Passwords do not match"
#
#         error_email = ''
#         v_email = ''
#         email = self.request.get("email")
#         if valid_email(email) or email == '':
#             v_email = email
#         else:
#             error_email = "Invalid email"
#
#         if (v_username == username and v_password != '' and
#                 v_verify == password and v_email == email):
#             User(user=v_username, pw=hash_str(v_password)).put()
#
#             self.response.headers.add_header('Set-Cookie', 'username=%s' % make_secure_val(str(username)))
#
#             self.redirect('/welcome')
#
#         else:
#
#
#             self.render("username.html", username=v_username,
#                         password=v_password,
#                         verify=v_verify,
#                         email=v_email,
#                         error_username=error_username,
#                         error_password=error_password,
#                         error_mismatch=error_mismatch,
#                         error_email=error_email)






class WelcomePage(Handler):
    """class for welcome page"""
    def get(self):
        """get method for displaying welome page"""
        username = self.request.cookies.get('username')

        if username:
            username = username.split('|')[0]

        if username:
            time.sleep(1)
            users = db.GqlQuery('Select * from User')
            comments = Comments.all()
            # posts = db.GqlQuery("SELECT * FROM BlogPost "
            #                     "ORDER BY created DESC")
            posts = BlogPost.all()
            posts.order('-created')

            self.render("welcome.html", users=users, username=username,
                        posts=posts, comments=comments)
        else:
            self.redirect('/')

    #def render_front(self, title='', content='', error='',):





class LoginPage(Handler):
    """loging class"""
    def get(self):
        """gets login form"""
        self.render('login.html')



    def post(self):
        """submits loging form"""
        username = self.request.get("username")
        password = self.request.get("password")

        qs1 = "Select * from User where user = '{}'".format(username)
        qry1 = db.GqlQuery(qs1)
        try:
            user_query = qry1[0].user
            pw_query = qry1[0].password
        except BaseException:
            user_query = None
            pw_query = None

        if username == user_query and hash_str(password) == pw_query:
            self.redirect("welcome")
            username_cookie = make_secure_val(str(username))
            self.response.headers.add_header('Set-Cookie', 'username=%s' % username_cookie)
        elif username == user_query and not password == pw_query:
            self.render('login.html', error_password='incorrect password', username=username)
        elif not username == user_query and password == pw_query:
            self.render('login.html', error_username='no username')
        else:
            self.render('login.html', error_username='no username')


class LogoutPage(Handler):
    """logout class"""
    def get(self):
        """sets value of cookie to ''"""
        self.response.headers.add_header('Set-Cookie', 'username=; Path =/')
        self.redirect('/login')

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
class Delete(Handler):
    """Delete Class"""
    def get(self, post_id):
        """method for deleting posts"""
        self.render('delete.html')
        username_cookie = self.request.cookies.get('username')
        if check_secure_val(username_cookie):
            key = db.Key.from_path('BlogPost', int(post_id))
            post = db.get(key)
            comments = Comments.all()
            comments.filter('post =', post_id)
            likes = Likes.all().filter('post =', post_id)


            if (post.user == username_cookie.split('|')[0] or
                    username_cookie.split('|')[0] == "Joshua"):
                post.delete()
                for comment in comments:
                    comment.delete()
                for like in likes:
                    like.delete()
                self.redirect('/welcome')
            else:
                self.redirect('/welcome')
        else:
            self.redirect('/welcome')
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

class Like(Handler):
    """Class is called to run the method below"""
    def get(self, post_id):
        """This is the method that is called when someone likes a post"""
        user_name_cookie = self.request.cookies.get('username')
        user = check_secure_val(user_name_cookie)
        if check_secure_val(user_name_cookie):
            like_index = Likes.all().filter('post =', post_id).filter('user =', user)
            try:
                current_user = like_index[0].user
            except BaseException:
                current_user = None
            if current_user == user:
                pass
            else:
                like = Likes(post=post_id, user=user)
                like.put()
        time.sleep(1)
        self.redirect('/permalink/{}'.format(str(post_id)))




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
