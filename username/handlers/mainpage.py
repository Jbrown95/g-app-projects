from handlers import handler
Handler = handler.Handler
class MainPage(Handler):
    """redirects to login"""
    def get(self):
        """assumes no cookie, redirects to login"""
        self.redirect('/login')
