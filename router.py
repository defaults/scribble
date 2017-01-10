import logging
import webapp2

from controllers import blog
from webapp2_extras import jinja2
from webapp2_extras import routes
from config import config


# method for handling errors
def error(request, response, exception):
    logging.exception(exception)
    params = {
        'error': exception
    }
    jinja = jinja2.get_jinja2()
    response.write(jinja.render_template('error.html', **params))


app = webapp2.WSGIApplication([
        routes.RedirectRoute(
            '/login/',
            handler=blog.LoginHandler,
            name='login',
            handler_method='login', strict_slash=True),
        routes.RedirectRoute(
            '/logout/',
            handler=blog.LoginHandler,
            name='logout',
            handler_method='logout', strict_slash=True),
        routes.RedirectRoute(
            '/<article_url>/',
            handler=blog.ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute(
            '/dashboard/',
            handler=blog.DashboardHandler, name='dashboard',
            strict_slash=True),
        routes.RedirectRoute(
            '/account/',
            handler=blog.AccountHandler, name='account',
            strict_slash=True),
        routes.RedirectRoute(
            '/short/<short_url>/',
            handler=blog.ShortUrlHandler, name='short_url',
            strict_slash=True),
        routes.RedirectRoute(
            '/',
            handler=blog.BlogHandler, name='blog',
            strict_slash=True),
], config=config.APPLICATION_CONFIG, debug=True)

# error handlers
app.error_handlers[404] = error
app.error_handlers[500] = error
