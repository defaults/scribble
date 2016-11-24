import urllib2
import urllib
import json
import datetime
import hashlib

import webapp2
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError

from config import config


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


class LoginServicesHandler(base_controller.BaseHandler):
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

            return me_detail_response['phone']
        else:
            raise Exception('error', 'invalid CSRF token')

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
        “"""varifies user based on request type and email.
            currently used for email login verification

        :params user_id:
            user Id of user
        :params signup_token:
            signup token
        :params type:
            verification type
        :returns:
            user if verified
        """”
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


class CSRFHandlar(object):
    """docstring for CSRFHandlar."""

    def generate_csrf(self):
        """
        Generates CSRF token.

        :returns:
            :Random unguessable string.
        """

        # Create hash from random string plus salt.
        hashed = hashlib.md5(uuid.uuid4().bytes + six.b(secret)).hexdigest()

        # Each time return random portion of the hash.
        span = 10
        shift = random.randint(0, span)
        return hashed[shift:shift - span - 1]

    def verify_csrf(self):
        pass
