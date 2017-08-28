from handlers import handler
"""handlers"""
Handler = handler.Handler
class LogoutPage(Handler):
    """logout class"""
    def get(self):
        """sets value of cookie to ''"""
        self.response.headers.add_header('Set-Cookie', 'username=; Path =/')
        self.redirect('/login')
