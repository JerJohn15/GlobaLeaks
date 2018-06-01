# Handle manipulation of submission states
import base64
import os

from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks

from globaleaks import models
from globaleaks.handlers.base import BaseHandler
from globaleaks.orm import transact
from globaleaks.utils.security import directory_traversal_check
from globaleaks.utils.utility import uuid4

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

class SubmissionStateCollection(BaseHandler):
    '''Handles submission states on the backend'''
    check_roles = 'admin'

    @inlineCallbacks
    def get(self):
        submission_states = yield retrieve_all_submission_states(self.request.tid)
        return submission_states
