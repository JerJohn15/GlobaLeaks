# -*- coding: utf-8 -*-
#
# Validates the token for password reset changes

from datetime import datetime, timedelta

from twisted.internet.defer import inlineCallbacks

from globaleaks import models
from globaleaks.handlers.base import BaseHandler
from globaleaks.orm import transact
from globaleaks.rest import requests
from globaleaks.utils.utility import datetime_now
from globaleaks.utils.security import generateRandomKey

from globaleaks.utils.security import change_password, generateRandomKey

@transact
def validate_password_reset(session, validation_token):
    '''transact version of db_validate_address_change'''
    return db_validate_password_reset(session, validation_token)


def db_validate_password_reset(session, validation_token):
    '''Retrieves a user given a password reset validation token'''
    user = session.query(models.User).filter(
        models.User.reset_password_token == validation_token,
        models.User.reset_password_date >= datetime.now() - timedelta(hours=72)
    ).one_or_none()

    if user is None:
        return False

    user.reset_password_token = None
    user.reset_password_date = datetime_now()
    user.password_change_needed = True

    return True

@transact
def generate_password_reset_token(session, tid, username, email):
    '''transact version of db_generate_password_reset_token'''

    return db_generate_password_reset_token(session, tid, username, email)

def db_generate_password_reset_token(session, tid, username, email):
    '''Generates a reset token against the backend'''

    user = session.query(models.User).filter(
        models.User.name == username,
        models.User.mail_address == email
    ).one_or_none()

class PasswordResetHandler(BaseHandler):
    check_roles = '*'
    redirect_url = "/#/login/resetpassword/successful"

    @inlineCallbacks
    def get(self, validation_token):
        check = yield validate_password_reset(validation_token)
        if not check:
            self.redirect_url = "/#/login/resetpassword/failure"

        self.redirect(self.redirect_url)

    @inlineCallbacks
    def post(self):
        request = self.validate_message(self.request.content.read(),
                                        requests.PasswordResetDesc)

        yield generate_password_reset_token(self.request.tid,
                                            request['username'],
                                            request['mail_address'])
        return None
