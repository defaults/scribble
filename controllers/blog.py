import datetime
import random
import re
import string
import json

import webapp2
from google.appengine.api import mail
from webapp2_extras import jinja2
from webapp2_extras import routes

from helpers import markdown
from models import model
from webapp2_extras import auth
from webapp2_extras import sessions
from config import config
from controllers import authentication
from controllers import base_controller


# base handler
class BlogHandler(base_controller.BaseHandler):

    def get(self):
        # code to search the database for blog posts
        article = model.Article.query().order(-model.Article.date)

        params = {
            'article': article
        }
        self.render_response('blog.html', **params)


class LoginHandler(base_controller.BaseHandler):
    def login(self):
        auth = self.auth
        if not auth.get_user_by_session():
            params = {
                'xsrf': authentication.CSRFHandlar().xsrf_token(
                    '/api/auth/login')
            }

            self.render_response('login.html', **params)
        else:

            self.redirect_to('dashboard')

    def logout(self):
        self.redirect_to(
            'login',
            message="Logged out! Login back to access account",
            message_type=sucess
        )

class FirstSetup(base_controller.BaseHandler):
    def setup(self):
        params = {
            'admin': auth.get_user_by_session(),
            'auth_secret': model.AuthSecret.to_json(True)
        }

        self.render_response('setup.html', **params)


# handler for serving article
class ArticleHandler(base_controller.BaseHandler):
    def get(self, **kwargs):
        article_url = kwargs['article_url']
        article_content = model.Article.query(
            model.Article.url == article_url).fetch()

        if article_content:
            for article in article_content:
                content = markdown.markdown(article.content,
                                            extras=["code-friendly"])
                tittle = article.tittle
                date = article.date
                url = article.url

            params = {
                'tittle': tittle,
                'content': content,
                'date': date,
                'url': url
            }
            self.render_response('article.html', **params)
        else:
            self.abort(404)

        return


# handler for writing blog
class WriteHandler(base_controller.BaseHandler):
    # add function to authenticate user

    @authentication.authenticated
    def get(self, **kwargs):
        params = {
            'xsrf': authentication.CSRFHandlar().xsrf_token(
                '/api/auth/login')
        }

        self.render_response('zenpen.html', **params)

        return


class DashboardHandler(base_controller.BaseHandler):
    """Main dashboard handlar"""

    # @authentication.authenticated
    def get(self):
        """Renders dashboard UI"""
        articles = {}
        user = {}
        config = {}
        params = {
            'page': 'dashboard',
            'articles': articles,
            'user': user,
            'account_config': config
         }
        self.render_response('dashboard.html', **params)


class AccountHandlar(base_controller.BaseHandler):
    """Account menegement page handlar"""
    @authentication.authenticated
    def get(self):
        user, account_config
        params = {
            'page': 'account',
            'user': user,
            'account_config': config
         }
        self.render_response('setting.html', **params)
