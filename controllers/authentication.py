from config import config
# from Cookie import CookieError, SimpleCookie
# from base64 import b64decode, b64encode
# import datetime
# import hashlib
# import hmac
# import logging
# import pickle
# import os
# import threading
# import time
#
# from google.appengine.api import memcache
# from google.appengine.ext import db
#
# # Configurable cookie options
# COOKIE_NAME_PREFIX = "SesS"  # identifies a cookie as being one used by gae-sessions (so you can set cookies too)
# COOKIE_PATH = "/"
# DEFAULT_COOKIE_ONLY_THRESH = 10240  # 10KB: GAE only allows ~16000B in HTTP header - leave ~6KB for other info
# DEFAULT_LIFETIME = datetime.timedelta(days=7)
#
# _tls = threading.local()
#
#
# def get_current_session():
#     """Returns the session associated with the current request."""
#     return _tls.current_session
#
#
# def set_current_session(session):
#     """Sets the session associated with the current request."""
#     _tls.current_session = session
#
#
# def is_gaesessions_key(k):
#     return k.startswith(COOKIE_NAME_PREFIX)
#
#
# class SessionModel(db.Model):
#     """Contains session data.  key_name is the session ID and pdump contains a
#     pickled dictionary which maps session variables to their values."""
#     pdump = ndb.BlobProperty()
#
#
# class RequestHandler(webapp2.RequestHandler):
#     """docstring for RequestHandler."""
#     def __init__(self, arg):
#         super(RequestHandler, self).__init__()
#         self.arg = arg


class LoginHandler():
    """docstring for LoginHandler."""
    def __init__(self, arg):
        super(LoginHandler, self).__init__()
        self.arg = arg

    def fb_accountkit_login(self, code, csrf):
        api_version = config.fb_account_kit['api_version']
        app_id = config.fb_account_kit['app_id']
        app_secret = config.fb_account_kit['app_secret']
        me_endpoint_base_url = config.fb_account_kit['me_endpoint_url']
        token_exchange_base_url = config.fb_account_kit['token_exchange_url']

        if CSRFHandlar.verify_csrf(csrf):
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

            if me_detail_response['phone']['number'] == config.admin['mobile']:
                return ({"phone_no": me_detail_response['phone']})
            else:
                raise Exception('erro', 'mobile number not allowed')


    def email_login(self):
        email = config.admin['admin_mail']

    class CSRFHandlar(object):
        """docstring for CSRFHandlar."""
        def __init__(self, arg):
            super(CSRFHandlar, self).__init__()
            self.arg = arg

        def generate_csrf(self):
            pass

        def verify_csrf(self):
            pass

    class AuthenticationHandler(object):
        """docstring for AuthenticationHandler."""
        def __init__(self, arg):
            super(AuthenticationHandler, self).__init__()
            self.arg = arg

        def authenticate(self):
            pass

        def deauthenticate(self):
            pass

        def authenticated(self):
            pass
