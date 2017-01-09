import webapp2
from webapp2_extras import routes

from controllers import blog_api
from config import config

app = webapp2.WSGIApplication([
        routes.RedirectRoute(
            '/api/articles',
            handler=blog_api.ArticleHandler,
            name='get_all_articles_api',
            handler_method='all_articles', methods=['GET'], strict_slash=True),
        routes.RedirectRoute(
            '/api/article',
            handler=blog_api.ArticleHandler, name='post_article_api',
            methods=['POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/article/<id>',
            handler=blog_api.ArticleHandler, name='article_api',
            methods=['GET', 'PUT', 'DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/api/subscribers',
            handler=blog_api.SubscriberHandler,
            name='get_all_subscribers_api',
            methods=['GET'], strict_slash=True),
        routes.RedirectRoute(
            '/api/subscriber',
            handler=blog_api.SubscriberHandler,
            name='post_subscriber_api', methods=['POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/subscriber/<id>',
            handler=blog_api.SubscriberHandler,
            name='subscriber_api', methods=['DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/api/tags',
            handler=blog_api.TagHandler, name='get_all_tags_api',
            methods=['GET'], strict_slash=True),
        routes.RedirectRoute(
            '/api/tag',
            handler=blog_api.TagHandler, name='post_tag_api',
            methods=['POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/tag/<id>',
            handler=blog_api.TagHandler, name='delete_tag_api',
            methods=['DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/api/short',
            handler=blog_api.UrlShortnerHandler, name='short_api',
            methods=['GET', 'POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/short/<id>',
            handler=blog_api.UrlShortnerHandler, name='delete_short_api',
            methods=['DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/api/auth/<authentication_type>/<authentication_token>',
            handler=blog_api.LoginApiHandler,
            name='verification_api',
            handler_method='verify', methods=['GET'], strict_slash=True),
        routes.RedirectRoute(
            '/api/auth/login',
            handler=blog_api.LoginApiHandler,
            name='login_api',
            handler_method='login', methods=['POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/auth/logout',
            handler=blog_api.LoginApiHandler,
            name='logout_api',
            handler_method='logout', methods=['GET'], strict_slash=True),
    ], config=config.APPLICATION_CONFIG, debug=True)
