import os
import jinja2
import webapp2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

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
