import urllib2
import urllib
import json
import datetime
import hashlib

import base64
import binascii
import hmac
import os
import time

import webapp2
from webapp2_extras import auth
from webapp2_extras import sessions
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db
from webapp2_extras.auth import InvalidAuthIdError

from config import config
from controllers import base_controller


def authenticated(handler):
    """
        Decorator that checks if there's a user associated with the
        current session. Will fail if there's no session present.
    """
    def check_authentication(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('login'), abort=True)
        else:
            return handler(self, *args, **kwargs)

        return check_authentication


class CSRFHandlar(base_controller.BaseHandler):
    """docstring for CSRFHandlar."""

    def __init__(self):
        # String used instead of user id when there is no user.
        # Not that it makes sense to protect unauthenticated
        # functionality from XSRF.
        self.ANONYMOUS_USER = 'anonymous'

        # DELIMITER character
        self.DELIMITER = ':'

        # 24 hours in seconds
        self.DEFAULT_TIMEOUT_SECS = 1*60*60*24

    def generate_token(self, key, user_id, path="", when=None):
        """Generates a URL-safe token for the given user, action, time tuple.
        Args:
        key: secret key to use.
        user_id: the user ID of the authenticated user.
        path: The path the token should be valid for.
        when: the time in seconds since the epoch at which the user was
          authorized for this action. If not set the current time is used.
        Returns:
        A string XSRF protection token.
        """
        when = when or int(time.time())
        digester = hmac.new(str(key))
        digester.update(str(user_id))
        digester.update(self.DELIMITER)
        digester.update(str(path))
        digester.update(self.DELIMITER)
        digester.update(str(when))
        digest = digester.digest()

        token = base64.urlsafe_b64encode('%s%s%d' % (digest,
                                                     self.DELIMITER,
                                                     when))
        return token

    def validate_token(self, key, token, user_id, path="", current_time=None,
                       timeout=-1):
        """Validates that the given token authorizes the user for the action.
        Tokens are invalid if the time of issue is too old or if the token
        does not match what generateToken outputs (i.e. the token was forged).
        Args:
        key: secret key to use.
        token: a string of the token generated by generateToken.
        user_id: the user ID of the authenticated user.
        path: The path the token was received on.
        current_time: Time at which the token was received (defaults to now)
        timeout: How long your tokens are valid in seconds before they time out
          (defaults to DEFAULT_TIMEOUT_SECS)
        Returns:
        A boolean - True if the user is authorized for the action, False
        otherwise.
        """
        if not token:
            return False
        if not timeout:
            timeout = self.DEFAULT_TIMEOUT_SECS
        try:
            decoded = base64.urlsafe_b64decode(str(token))
            token_time = long(decoded.split(self.DELIMITER)[-1])
        except (TypeError, ValueError):
            return False
        if current_time is None:
            current_time = time.time()
        # If the token is too old it's not valid.
        if current_time - token_time > timeout:
            return False

        # The given token should match the generated one with the same time.
        expected_token = generate_token(
            key, user_id, path=path, when=token_time)
        return const_time_compare(expected_token, token)

    @staticmethod
    def const_time_compare(a, b):
        """Compares the the given strings in constant time."""
        if len(a) != len(b):
            return False

        equals = 0
        for x, y in zip(a, b):
            equals |= ord(x) ^ ord(y)

        return equals == 0

    def xsrf_protect(self, func):
        """Decorator to protect webapp2's get and post functions from XSRF.
        Decorating a function with @xsrf_protect will verify that a valid
        XSRF token has been submitted through the xsrf parameter.
        Both GET and POST parameters are accepted.
        If no token or an invalid token is received,
        the decorated function is not called and a 403 error will be issued.
        """
        this = self

        def decorate(self, *args, **kwargs):
            path = os.environ.get('PATH_INFO', '/')
            token = self.request.get('xsrf', None)
            if not token:
                self.error(403)
                return

            user = this.ANONYMOUS_USER
            if users.get_current_user():
                user = users.get_current_user().user_id()
            if not this.validate_token(config.CSRF_SECRET_KEY,
                                       token, user, path):
                self.error(403)
                return

            return func(self, *args, **kwargs)

        return decorate

    def xsrf_token(self, path=None):
        """Generates an XSRF token for the given path.
        This function is mostly supposed to be used as a filter for a
        templating system, so that tokens can be conveniently generated
        directly in the template.
        Args:
        path: The path the token should be valid for. By default,
        the path of the current request.
        """
        user = self.ANONYMOUS_USER
        if not path:
            path = os.environ.get('PATH_INFO')
        if users.get_current_user():
            user = users.get_current_user().user_id()

        return self.generate_token(config.CSRF_SECRET_KEY, user, path)


class LoginServicesHandler(CSRFHandlar):
    """login handlar - handler all types of login."""

    def accountkit_login(self, code, csrf):
        """Initialtes fb accountkit mobile no based login

        :params code:
            code to verify login request
        :params csrf:
            csrf nonce
        :returns:
            logged in mobile_no
        """
        api_version = config.CONFIG.fb_accountkit_api_version
        app_id = config.CONFIG.fb_account_kit_app_id
        app_secret = config.CONFIG.fb_account_kit_app_secret
        me_endpoint_base_url = config.CONFIG.fb_account_kit_endpoint_url
        token_exchange_base_url = \
            config.CONFIG.fb_account_kit_token_exchange_url

        app_access_token = '|'.join(['AA', app_id, app_secret])
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'access_token': app_access_token
        }

        token_exchange_url = token_exchange_base_url + '?' + \
            urllib.urlencode(params)
        token_exchange_req = urllib2.urlopen(token_exchange_url)
        token_exchange_result = json.loads(token_exchange_req.read()
                                           .decode('utf-8'))
        me_endpoint_url = me_endpoint_base_url + '?access_token=' + \
            token_exchange_result['access_token']
        me_detail_request = urllib2.urlopen(me_endpoint_url)
        me_detail_response = json.loads(me_detail_request
                                        .read().decode('utf-8'))

        return me_detail_response['phone']

    def initiate_email_login(self, user):
        """Initialtes email based login by sending verification mail

        :params user:
            user
        :returns:
            status(boolean)
        """
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)
        verification_url = self.uri_for(
            'verification', type='signup', user_id=user_id,
            signup_token=token, _full=True)

        valid_till = datetime.time.now()

        email_payload = {
            'verification_url': verification_url,
            'valid_till': valid_till
        }

        self.send_email(user.email, email_type='signup', payload=email_payload)

        return

    def verify_user(self, user_id, signup_token, type):
        """varifies user based on request type and email.
            currently used for email login verification

        :params user_id:
            user Id of user
        :params signup_token:
            signup token
        :params type:
            verification type
        :returns:
            user if verified
        """
        user, ts = self.user_model.get_by_auth_token(
            int(user_id), signup_token, 'signup')

        if not user:
            logging.info(
                'Could not find any user with id "%s" signup token "%s"',
                user_id, signup_token)
            raise Exception('error', 'Could not find any user')

        # store user data in the session
        self.auth.set_session(
            self.auth.store.user_to_dict(user), remember=True)

        if type == 'signup':
            self.user_model.delete_signup_token(user.get_id(), signup_token)

        if not user.verified:
            user.verified = True
            user.put()

        return user
