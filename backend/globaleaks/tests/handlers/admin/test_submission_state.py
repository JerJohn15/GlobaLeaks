# -*- coding: utf-8 -*-
import json

from globaleaks.handlers.admin import submission_states
from globaleaks.jobs.delivery import Delivery
from globaleaks.rest import requests
from globaleaks.tests import helpers
from twisted.internet.defer import inlineCallbacks


class SubmissionStateCollectionDesc(helpers.TestHandlerWithPopulatedDB):
    _handler = submission_states.SubmissionStateCollection

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestHandlerWithPopulatedDB.setUp(self)

    @inlineCallbacks
    def test_get(self):
        handler = self.request({}, role='admin')
        response = yield handler.get()

        print(response)
