import random
import re
import string
import json
from datetime import datetime

import webapp2
from google.appengine.api import mail
from webapp2_extras import jinja2
from webapp2_extras import routes
from webapp2_extras import sessions
from google.appengine.datastore.datastore_query import Cursor

from helpers import markdown
from helpers import short_url
from models import model
from config import config
from controllers import authentication
from controllers import base_controller


class BlogApiHandler(base_controller.JsonRestHandler):
    """Base handler for blog API"""

    @staticmethod
    def url_shortner(full_url):
        """Method for sortning full URL and saving and returning short URL"""
        short_url = ''.join(random.choice(string.ascii_letters +
                                          string.digits) for _ in range(10))
        save = model.ShortUrl(full_url=full_url,
                              short_url=short_url)
        save.put()
        return short_url


class LoginApiHandler(BlogApiHandler):
    """login api handler - handles login and logout"""

    @xsrf_protect
    def login(self):
        login_type = self.request.get('login_type')
        try:
            if login_type == 'fb_accountkit':
                code = self.request.get('code')

                authenticated_mobile_no = \
                    authentication.LoginServicesHandler().accountkit_login(
                        code, csrf)

                user = self.user_model.get_by_mobile_no(
                    authenticated_mobile_no)

                self.final_processor(user, 'fb_accountkit',
                                     authenticated_mobile_no)

            elif login_type == 'email':
                email = self.request.get('email')
                user = self.user_model.get_by_email_address(email)
                self.final_processor(user, 'email', email)

                self.send_success({'status': 'success'})

            else:
                self.send_error(401, 'login type not supported')

        except Exception as e:
            self.send_error(500, e)

    def logout(self):
        self.auth.unset_session()
        self.redirect_to('home')

    def create_user(self, username, name, email, mobile_no, verified=False):
        status, created_user = self.user_model.create_user(
                                        username,
                                        ['email_address', 'mobile_no'],
                                        name=name,
                                        email_address=email,
                                        mobile_no=mobile_no,
                                        verified=varified)

        if status:
            return created_user
        else:
            raise Exception('user creation failed')

    def final_processor(user, login_type, authenticated_identifier):
        """finallly checks for valid user and redirects after login.
        :param user:
            user object
        :param login_type:
            user login_type
        :param authenticated_identifier:
            user identifier by which user is authenticated
        """
        if user:
            if not user.verified:
                user.verified = True
                user.put()
            self.auth.set_session(
                self.auth.store.user_to_dict(user))
            self.redirect_to('dashboard')

        elif (login_type == 'fb_accountkit' and
              config.ADMIN['mobile_no'] == authenticated_identifier) or \
            (login_type == 'email' and
             config.ADMIN.mobile == authenticated_identifier):
            self.user_model.create_user(
                config.admin, verified=True)
            self.redirect_to('first_time_setup')

        else:
            self.send_error(404, {
                    'status': 'failure',
                    'message': 'user not recognised/allowed.'
                })


class ArticleHandler(BlogApiHandler):
    """Article handler - Provides an api for working with articles"""

    def all_articles(self):
        """
        GET request to get all articles - Exposed as `GET /api/articles`
        """
        try:
            cursor = Cursor(urlsafe=self.request.get('cursor'))
            reverse = bool(self.request.get('reverse'))
            limit = self.request.get('limit', default_value=5)
            with_deleted = bool(self.request.get('with_deleted'))
            deleted = bool(self.request.get('deleted'))
            tags = self.request.get_all('tags')
            query = model.Article.query(model.Article.soft_deleted == deleted)
            if tags:
                query = model.Article \
                    .query(model.Article.soft_deleted == deleted,
                           model.Article.tags.IN(tags))
            if with_deleted:
                query = model.Article.query()
                if tags:
                    query = model.Article.query(model.Article.tags.IN(tags))
            final_query = query.order(-model.Article.created_on)
            if reverse:
                final_query = query.order(model.Article.created_on)
            articles, next_cursor, more = final_query.fetch_page(
                                                limit, start_cursor=cursor)
            if articles:
                articles.append(next_cursor.urlsafe())
                articles.append(more)
            self.send_success(articles)
        except Exception as e:
            self.send_error(500, e)

    def get(self, **kwargs):
        """
        GET request to get article by id - Exposed as `GET /api/article/<id>`
        """
        try:
            # TODO get user from session and verify
            id = kwargs['id']
            article = model.Article.get_by_id(long(id))
            if article:
                self.send_success(article)
            else:
                raise TypeError
        except TypeError as te:
            self.send_error(404, 'Resource not found')
        except Exception as e:
            self.send_error(500, e)

    @authenticated
    def post(self):
        """POST method for articles - Exposed as `POST /api/article`"""
        try:
            article = model.Article()
            article.from_json(self.request.body)
            article.url = re.sub(
                        r'[/|!|"|:|;|.|%|^|&|*|(|)|@|,|{|}|+|=|_|?|<|>]',
                        'p', article.tittle).replace(' ', '-').lower()
            article.short_url = 'hii'
            article.put()
            self.send_success(article)
        except Exception as e:
                self.send_error(404, e)

    @authenticated
    def put(self, **kwargs):
        """
        PUT method for article - Exposed as `PATCH /api/article/<id>/`
        """
        try:
            id = kwargs['id']
            article = model.Article.get_by_id(long(id))
            if article:
                article.from_json(self.request.body)
                article.modified_on = datetime.now()
                article.put()
                self.send_success(article)
            else:
                raise IndexError
        except ValueError as ve:
            self.send_error(404, 'invalid literal')
        except IndexError as e:
            self.send_error(504, 'wrong index')
        except Exception as e:
            self.send_error(500, e)

    @authenticated
    def delete(self, **kwargs):
        """
        DELETE method for articles - Exposed as `DELETE /api/article/<id>`
        """
        try:
            id = kwargs['id']
            article = model.Article.get_by_id(long(id))
            if article:
                article.soft_deleted = True
                article.put()
                self.send_success({'status': 'success'})
            else:
                raise IndexError
        except IndexError as ie:
            self.send_error(404, 'wrong index')
        except Exception as e:
            self.send_error(500, e)


class SubscriberHandler(BlogApiHandler):
    """
    Handler for subscribers - Exposes GET, POST, PATCH,
    DELETE for `/api/subscriber`
    """
    @authenticated
    def get(self):
        """G
        ET method for subscribers - Exposed as `GET /api/subscribers`
        """
        try:
            article = model.Subscriber.query().fetch()
            self.send_success(article)
        except Exception as e:
            self.send_error(500, e)

    def post(self):
        """
        POST method for subscribers - Exposed as `POST /api/subscriber`
        """
        try:
            subscriber = model.Subscriber()
            subscriber.from_json(self.request.body)
            subscriber.put()
            self.send_success(subscriber)
        except Exception as e:
            self.send_error(500, e)

    @authenticated
    def delete(self, **kwargs):
        """
        DELETE method for subscribers -
        Exposed as `DELETE /api/subscriber/<id>`
        """
        try:
            id = kwargs['id']
            subscriber = model.Subscriber.get_by_id(long(id))
            if subscriber:
                subscriber.soft_deleted = True
                self.send_success({'status': 'success'})
            else:
                raise IndexError
        except IndexError as ie:
            self.send_error(404, 'wrong index')
        except Exception as e:
            self.send_error(500, e)


class TagHandler(BlogApiHandler):
    """
    Blog tag handler -
    Exposes api for GET, POST, DELETE
    """
    def get(self):
        """
        GET method for all tags - Exposed as `GET /api/tag`
        """
        try:
            tags = model.Tag.query().fetch()
            self.send_success(tags)
        except Exception as e:
            self.send_error(500, e)

    @authenticated
    def post(self):
        """
        POST method for all tags - Exposed as `POST /api/tag`
        """
        try:
            tag = model.Tag()
            tag.from_json(self.request.body)
            tag.put()
            self.send_success(tag)
        except Exception as e:
            self.send_error(500, e)

    @authenticated
    def delete(self, **kwargs):
        """
        DELETE method for all tags - Exposed as `DELETE /api/tag/<id>`
        """
        try:
            id = kwargs['id']
            tag = model.Tag.get_by_id(long(id))
            if tag:
                tag.soft_deleted = True
                tag.put()
                self.send_success({'status': 'success'})
            else:
                raise IndexError
        except IndexError as e:
            self.send_error(404, 'wrong index')
        except Exception as e:
            self.send_error(500, e)


class UrlShortnerHandler(BlogApiHandler):
    """
    URL shortner API handler -
    Exposes GET and POST API
    """

    def get(self):
        """
        GET method for url shortner -
        Exposed as `GET /api/short?short_url=<shortUrl>`
        """
        try:
            short_url_string = self.request.get('short_url')
            long_url_string = self.request.get('long_url')
            if short_url_string:
                short_url_id = short_url.saturate(short_url_string)
                short_url_obj = model.ShortUrl.get_by_id(short_url_id)
                short_url_obj.short_url = short_url\
                    .dehydrate(short_url_obj.key.id())
                self.send_success(short_url_obj)
            elif long_url_string:
                short_url_obj = model.ShortUrl \
                    .query(model.ShortUrl.full_url == long_url).get()
                short_url_obj.short_url = short_url\
                    .dehydrate(short_url_obj.key.id())
                self.send_success(short_url_obj)
        except Exception as e:
            self.send_error(500, e)

    @authenticated
    def post(self):
        """
        POST method for url shortner -
        Exposed as `POST /api/short>`
        """
        try:
            short_url_obj = model.ShortUrl()
            short_url_obj.from_json(self.request.body)
            short_url_exists = \
                model.ShortUrl.query(model.ShortUrl.full_url ==
                                     short_url_obj.full_url).get()
            if short_url_exists:
                short_url_link = short_url.dehydrate(short_url_exists.key.id())
                short_url_exists.short_url = short_url_link
                self.send_success(short_url_exists)
            else:
                short_url_obj.put()
                short_url_link = short_url.dehydrate(short_url_obj.key.id())
                short_url_obj.short_url = short_url_link
                self.send_success(short_url_obj)
        except Exception as e:
            self.send_error(500, e)

    @authenticated
    def delete(self, **kwargs):
        """
        DELETE method for url shortner -
        Exposed as `DELETE /api/short/<id>`
        """
        try:
            id = kwargs['id']
            short_url_obj = model.ShortUrl.get_by_id(long(id))
            if short_url_obj:
                short_url_obj.soft_deleted = True
                short_url_obj.put()
                self.send_success({'status': 'success'})
            else:
                raise IndexError
        except IndexError as ie:
            self.send_error(404, 'wrong index')
        except Exception as e:
            self.send_error(500, e)


def ConfigHandlar(BlogApiHandler):
    """
    Configuration
     get and update handlar
    """
    @authenticated
    def get(self):
        """
        GET method for user config (available for admin) -
        Exposed as `GET /api/config`
        """
        pass

    @authenticated
    def post(self):
        """
        POST method for user config (available for admin) -
        Exposed as `POST /api/config`
        """
        pass

    @authenticated
    def put(self):
            """
            PATCH/PUT method for user config (available for admin) -
            Exposed as `PATCH /api/config`
            """
        pass
