import datetime
import random
import json

from google.appengine.api import mail
from config import config


@staticmethod
def send_email(receiver_address, email_subject, email_body):
    """method to send mail"""
    # get email api authrised sender
    sender_address = (
                '<{}@appspot.gserviceaccount.com>'.format(
                    app_identity.get_application_id()))

    # send mail
    mail.send_mail(sender=sender_address,
                   to=receiver_address,
                   subject=email_subject,
                   body=email_body)

    return
