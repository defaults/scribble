import json
import logging
import datetime
import types
import uuid
from datetime import datetime
import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb

from webapp2_extras import security

from google.appengine.api import images
from google.appengine.ext import ndb


class JsonifiableEncoder(json.JSONEncoder):
    """JSON encoder"""
    def default(self, obj):
        if isinstance(obj, Jsonifiable):
            result = json.loads(obj.to_json())
            return result


class Jsonifiable:
    """
    JSON encoder which provides a convenient extension point for custom JSON
    encoding of Jsonifiable subclasses.
    """

    @staticmethod
    def lower_first(key):
        """Make the first letter of a string lower case."""
        return key[:1].lower() + key[1:] if key else ''

    @staticmethod
    def transform_to_camelcase(key):
        """
        Transform a string underscore separated words
        to concatenated camel case.
        """
        return Jsonifiable.lower_first(
            ''.join(c.capitalize() or '_' for c in key.split('_')))

    @staticmethod
    def transform_from_camelcase(key):
        """
        Tranform a string from concatenated camel case to
        underscore separated words.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def to_json(self):
        """
        Converts object to json.
        """
        result = {}
        a = self
        properties = self.to_dict()
        # properties = dict(properties, **dict(id=self.key.id()))
        if isinstance(self, ndb.Model):
            properties['id'] = unicode(self.key.id())
        for key, value in properties.iteritems():
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            result[Jsonifiable.transform_to_camelcase(key)] = value
        return json.dumps(result)

    def from_json(self, json_string):
        """Sets properties on this object based on the JSON string supplied."""
        o = json.loads(json_string)
        properties = {}
        if isinstance(self, ndb.Model):
            properties = self._properties
        for key, value in o.iteritems():
            property_value = value
            property_key = Jsonifiable.transform_from_camelcase(key)
            if property_key in properties.keys():
                if isinstance(properties[property_key], ndb.IntegerProperty):
                    property_value = int(value)
                if isinstance(properties[property_key], ndb.DateTimeProperty):
                    property_value = datetime.strptime(value,
                                                       "%Y-%m-%d %H:%M:%S")
            self.__setattr__(property_key, property_value)


class Article(ndb.Model, Jsonifiable):
    """Represents article written"""
    url = ndb.StringProperty()
    tittle = ndb.StringProperty()
    date = ndb.DateTimeProperty(default=datetime.now())
    content = ndb.TextProperty()
    short_url = ndb.StringProperty()
    stars = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)
    published = ndb.BooleanProperty(default=True)
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class Subscriber(ndb.Model, Jsonifiable):
    """Represents subscribers of blog"""
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class ShortUrl(ndb.Model, Jsonifiable):
    """Represents short url for blog"""
    full_url = ndb.StringProperty()
    short_url = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class Tag(ndb.Model, Jsonifiable):
    """Represents tags for blog"""
    tag = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class Auth(ndb.Model, Jsonifiable):
    """Represents Authorisation token for verifing user"""
    token = ndb.StringProperty()
    token_type = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class User(webapp2_extras.appengine.auth.models.User):
    """User model extending webapp2 auth expando user model"""
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=False)
    email_address = ndb.StringProperty(indexed=True)
    mobile_no = ndb.StringProperty(indexed=True)
    is_admin = ndb.BooleanProperty(indexed=True, default=False)
    timezone = ndb.StringProperty(default='UTC')

    @classmethod
    def add_new_user(cls, user_data, verified=False):
        """Creates new user

        :param user_data:
            Dict containing user data to save.
        :param verified:
            Boolean value if user verified or not.
        :returns:
            A tuple ``(User, timestamp)``, with status and user object
        """

        status, user_data = cls.create_user(
                        user_data['email'],
                        ['email_address', 'mobile_no'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        email_address=user_data['email'],
                        mobile_no=user_data['mobile'],
                        verified=verified)

        return status, user_data

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            A tuple ``(User, timestamp)``, with a user object and
            the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None

    @classmethod
    def get_by_email_address(cls, email):
        """Returns a user object based on email_address(unique property).

        :param email:
            The email_address of the requesting user.
        :returns:
            User object.
        """
        return cls.query(cls.email_address == email).get()

    @classmethod
    def get_by_mobile_no(cls, mobile_no):
        """Returns a user object based on mobile_no(unique property).
        :param mobile_no:
            The mobile of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            User object
        """
        return cls.query(cls.mobile_no == mobile_no).get()


class AuthConfig(ndb.Model, Jsonifiable):
    """Model for datastore to store the Authentication config."""
    google_analytics_id = ndb.StringProperty()
    fb_accountkit_api_version = ndb.StringProperty(default='v1.0')
    fb_accountkit_app_id = ndb.StringProperty(default='')
    fb_accountkit_app_secret = ndb.StringProperty(default='')
    fb_accountkit_me_endpoint_url = ndb.StringProperty(
        default='https://graph.accountkit.com/v1.0/me')
    fb_accountkit_token_exchange_url = ndb.StringProperty(
        default='https://graph.accountkit.com/v1.0/access_token')
    github_client_id = ndb.StringProperty(
        default='')
    github_client_secret = ndb.StringProperty(
        default='')

    @property
    def is_fb_accountkit_login_enabled(self):
        """return """
        return bool(
            self.fb_accountkit_app_id and self.fb_accountkit_app_secret)

    @property
    def github_login_enabled(self):
        return bool(x=self.github_client_id and self.github_client_secret)


class Config(ndb.Model):
    csrf_secret_key = ndb.StringProperty(
        indexed=True, default=uuid.uuid4().hex)

    @classmethod
    def get_master_db(cls):
        return cls.get_or_insert('master')

    @staticmethod
    def get_csrf_secret_key():
        """Retrieves the XSRF secret.

        Tries to retrieve the XSRF secret from memcache, and if that fails,
        falls back to getting it out of datastore. Note that the secret
        should not be changed, as that would result in all issued
        tokens becoming invalid.
        """
        secret = memcache.get('xsrf_secret')
        if not secret:
            xsrf_secret = Config.all().get()
            if not xsrf_secret:
                secret = binascii.b2a_hex(os.urandom(16))
                xsrf_secret = XsrfSecret(secret=secret)
                xsrf_secret.put()

                secret = xsrf_secret.secret
                memcache.set('xsrf_secret', secret)

        return secret
