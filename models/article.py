import datetime
import logging
from collections import defaultdict

from google.cloud import datastore
import google.cloud.exceptions

def article():
    pass

class Article(ndb.Model, Jsonifiable):
    """Represents article written"""
    url = ndb.StringProperty(indexed=True)
    tittle = ndb.StringProperty()
    date = ndb.DateTimeProperty(default=datetime.now())
    content = ndb.TextProperty(indexed=False)
    short_url = ndb.StringProperty(indexed=True)
    stars = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)
    published = ndb.BooleanProperty(default=True)
    created_on = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False, indexed=True)
