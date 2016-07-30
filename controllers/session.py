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
