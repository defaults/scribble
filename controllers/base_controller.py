import random
import re
import string
import json
import os
from datetime import datetime

import urllib
import urllib2

import webapp2
import jinja2
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError

from config import config

from google.appengine.api import mail
from webapp2_extras import routes
from webapp2_extras import sessions

from helpers import markdown
from helpers import short_url
from models import model
from config import config


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(
        'public/build/')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# method for handling errors
def error_handlar(request, response, exception):
    params = {
        'error': exception,
        'meta': {}
    }
    template = JINJA_ENVIRONMENT.get_template('templates/error.html')
    response.write(template.render(params))


class BaseHandler(webapp2.RequestHandler):
    """docstring for BaseHandler."""

    def warmup(self):
        self.response.headers["Content-Type"] = "application/json"

        self.response.write({'status': 'success'})

    def dispatch(self):
        # Get a session store for this request
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.
        The list of attributes to store in the session is specified in
        config['webapp2_extras.auth']['user_attributes'].
        :returns
            A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.
        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.
        :returns
            The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.
        It is consistent with config['webapp2_extras.auth']['user_model'],
        if set.
        """
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    @webapp2.cached_property
    def jinja2(self):
        """Returns a Jinja2 renderer cached in the app registry."""
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **params):
        """Renders a template and writes the result to the response."""

        default_meta = {}
        # print "hi" +  default_meta
        # if params.has_key('meta'):
        #     params['meta'].update(default_meta)
        # else:
        params['meta'] = {}

        template = JINJA_ENVIRONMENT.get_template('templates/' + _template)
        self.response.write(template.render(**params))

    def send_email(self, email, email_type, payload):
        """method to send mail"""
        # get email api authrised sender
        sender_address = (
                    '<{}@appspot.gserviceaccount.com>'.format(
                        app_identity.get_application_id()))

        subject, email_body = self.generate_email(email_type, payload)

        mail.send_mail(sender=sender_address,
                       to=email,
                       subject=subject,
                       body=email_body)

        return

    def generate_email(email_type, payload):
        """generates email body
        :params email_type:
            type of email
        :params payload:
            object having email payload

        returns:
            text/html
        """
        pass


class JsonRestHandler(BaseHandler):
    """
    Base RequestHandler type which provides convenience methods for writing
    JSON HTTP responses.
    """
    JSON_MIMETYPE = "application/json"

    def send_error(self, code, message):
        """
        Convenience method to format an HTTP error response in a standard
        format.
        """
        self.response.set_status(code, message)
        self.response.out.write(message)
        return

    def send_success(self, obj=None):
        """
        Convenience method to format a PhotoHunt JSON HTTP response in a
        standard format.
        """
        self.response.headers["Content-Type"] = "application/json"
        if obj is not None:
            if isinstance(obj, basestring):
                self.response.out.write(obj)
            else:
                self.response.out.write(json.dumps(obj,
                                        cls=model.JsonifiableEncoder))
        else:
            self.response.out.write('[]')
