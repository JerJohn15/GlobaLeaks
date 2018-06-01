# -*- coding: utf-8 -*-
import json

from globaleaks import models
from globaleaks.handlers.admin import submission_states
from globaleaks.jobs.delivery import Delivery
from globaleaks.rest import requests
from globaleaks.tests import helpers
from twisted.internet.defer import inlineCallbacks

from globaleaks.orm import transact

@transact
def count_submission_states(session, tid):
    return session.query(models.SubmissionStates).filter(
        models.SubmissionStates.tid==tid).count()

class SubmissionStateCollectionDesc(helpers.TestHandlerWithPopulatedDB):
    _handler = submission_states.SubmissionStateCollection

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestHandlerWithPopulatedDB.setUp(self)

    @inlineCallbacks
    def test_get(self):
        handler = self.request({}, role='admin')
        response = yield handler.get()

        self.assertEqual(len(response), 3)

    @inlineCallbacks
    def test_post(self):
        # Create a submission state
        data_request = {
            'submission_state': 'test_state'
        }
        handler = self.request(data_request, role='admin')
        yield handler.post()

        session_state_count = yield count_submission_states(1)
        self.assertEqual(session_state_count, 4)
