# Handle manipulation of submission states
import base64
import os
import uuid

from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks

from globaleaks import models
from globaleaks.handlers.base import BaseHandler
from globaleaks.orm import transact
from globaleaks.rest import requests
from globaleaks.utils.security import directory_traversal_check
from globaleaks.utils.utility import uuid4

from six import text_type

def serialize_submission_state(row):
    submission_state = {
        'id': row.id,
        'tid': row.tid,
        'submission_state': row.submission_state
    }

    return submission_state

@transact
def retrieve_all_submission_states(session, tid):
    '''Retrieves all submission states'''
    submission_states = []

    rows = session.query(models.SubmissionStates).filter(models.SubmissionStates.tid == tid)
    for row in rows:
        submission_states.append(
            serialize_submission_state(row)
        )
    return submission_states

@transact
def create_submission_state(session, tid, request):
    '''Creates submission state'''
    new_state = models.SubmissionStates()
    new_state.id = text_type(uuid.uuid4())
    new_state.tid = tid
    new_state.submission_state = request['submission_state']

    session.add(new_state)
    session.commit()

class SubmissionStateCollection(BaseHandler):
    '''Handles submission states on the backend'''
    check_roles = 'admin'

    @inlineCallbacks
    def get(self):
        submission_states = yield retrieve_all_submission_states(self.request.tid)
        return submission_states

    @inlineCallbacks
    def post(self):
        request = self.validate_message(self.request.content.read(),
                                        requests.SubmissionStateDesc)

        yield create_submission_state(self.request.tid, request)
        return None
