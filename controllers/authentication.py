import urllib2
import urllib
import json

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


class LoginServicesHandler():
    """docstring for LoginHandler."""

    # fb accountkit login method
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
                return ({"user": me_detail_response['phone']})
            else:
                raise Exception('error', 'mobile number not allowed')
        else:
            raise Exception('error', 'invalid CSRF token')

    # email based login method
    def email_login(self):
        email = config.admin['admin_mail']
        verify = model.Auth.query(model.Auth.type == 'email_token',
                                  model.auth.soft_deleted == false).get()

        if not verify:
            token = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for _ in range(20))
            save = model.Auth(token=token)
            save.put()

        auth_url = uri_for('login_api', page='email', format=token)
        to = config.admin['admin_name'] + ' ' + '<' + \
            config.admin['admin_mail'] + '>'
        subject = 'Link to write blog'
        body = 'https://blog.vikashkumar.me/write/{0}'.format(verify.token)

        # helpers.send_email(to, subject, body)
        return ({'status': 'success'})

    # github oauth login method
    def github_oauth_login(self):
        pass


class CSRFHandlar(object):
    """docstring for CSRFHandlar."""

    def generate_csrf(self):
        pass

    def verify_csrf(self):
        pass
