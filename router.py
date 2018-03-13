import logging
import webapp2

from controllers import blog
from controllers import base_controller
from webapp2_extras import jinja2
from webapp2_extras import routes
from config import config




app = webapp2.WSGIApplication([
    routes.RedirectRoute(
        '/_ah/warmup', handler=base_controller.BaseHandler,
        name='warmup', handler_method='warmup'),
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
        '/welcome/',
        handler=blog.FirstSetup,
        name='first_time_setup',
        handler_method='setup', strict_slash=True),
    routes.RedirectRoute(
        '/dashboard/',
        handler=blog.DashboardHandler, name='dashboard',
        strict_slash=True),
    routes.RedirectRoute(
        '/account/',
        handler=blog.AccountHandlar, name='account',
        strict_slash=True),
    routes.RedirectRoute(
        '/<article_url>/',
        handler=blog.ArticleHandler, name='article', strict_slash=True),
    routes.RedirectRoute(
        '/',
        handler=blog.BlogHandler, name='blog',
        strict_slash=True),
], config=config.APPLICATION_CONFIG, debug=True)

# error handlers
app.error_handlers[404] = base_controller.error_handlar
app.error_handlers[500] = base_controller.error_handlar
