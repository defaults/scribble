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
            '/login',
            handler=blog.LoginHandler,
            name='login',
            handler_method='login', strict_slash=True),
        routes.RedirectRoute(
            '/logout',
            handler=blog.LoginHandler,
            name='logout',
            handler_method='logout', strict_slash=True),
        routes.RedirectRoute(
            '/auth/<token>/',
            handler=blog.WriteHandler, name='write', strict_slash=True),
        routes.RedirectRoute(
            '/<article_url>/',
            handler=blog.ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute(
            '/write/resend_mail',
            handler=blog.BlogHandler, name='resend_mail',
            handler_method='resend_mail', strict_slash=True),
        routes.RedirectRoute(
            '/dashboard/',
            handler=blog.DashboardHandler, name='dashboard',
            strict_slash=True),
        routes.RedirectRoute(
            '/short/<short_url>',
            handler=blog.ShortUrlHandler, name='short_url',
            strict_slash=True),
        routes.RedirectRoute(
            '/',
            handler=blog.ArticlesListHandler, name='blog',
            strict_slash=True),
], config=config.application_config, debug=True)

# errors
app.error_handlers[404] = error
app.error_handlers[500] = error
