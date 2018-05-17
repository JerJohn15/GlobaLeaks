# -*- coding: utf-8 -*-

from globaleaks import __version__
from globaleaks.handlers.admin import node
from globaleaks.models.config import NodeL10NFactory
from globaleaks.rest.errors import InputValidationError
from globaleaks.tests import helpers
from twisted.internet.defer import inlineCallbacks

# special guest:
stuff = u"³²¼½¬¼³²"


class TestNodeInstance(helpers.TestHandlerWithPopulatedDB):
    _handler = node.NodeInstance

    @inlineCallbacks
    def test_get(self):
        handler = self.request(role='admin')
        response = yield handler.get()

        self.assertTrue(response['version'], __version__)

    @inlineCallbacks
    def test_get_receiver_with_priv_acl(self):
        handler = self.request(role='receiver')
        response = yield handler.get()

        self.assertNotIn('version', response)
        self.assertIn('header_title_submissionpage', response)

    @inlineCallbacks
    def test_put_update_node(self):
        self.dummyNode['hostname'] = 'blogleaks.blogspot.com'

        for attrname in NodeL10NFactory.keys:
            self.dummyNode[attrname] = stuff

        handler = self.request(self.dummyNode, role='admin')
        response = yield handler.put()

        self.assertTrue(isinstance(response, dict))
        self.assertTrue(response['version'], __version__)

        for response_key in response.keys():
            # some keys are added by GLB, and can't be compared
            if response_key in ['creation_date',
                                'acme',
                                'https_enabled',
                                'languages_supported',
                                'version', 'version_db',
                                'latest_version',
                                'configured', 'wizard_done',
                                'receipt_salt', 'languages_enabled',
                                'root_tenant', 'https_possible',
                                'hostname', 'onionservice']:
                continue

            self.assertEqual(response[response_key],
                             self.dummyNode[response_key])

    @inlineCallbacks
    def test_put_update_node_invalid_lang(self):
        self.dummyNode['languages_enabled'] = ["en", "shit"]
        handler = self.request(self.dummyNode, role='admin')

        yield self.assertFailure(handler.put(), InputValidationError)

    @inlineCallbacks
    def test_put_update_node_languages_with_default_not_compatible_with_enabled(self):
        self.dummyNode['languages_enabled'] = ["fr"]
        self.dummyNode['default_language'] = "en"
        handler = self.request(self.dummyNode, role='admin')

        yield self.assertFailure(handler.put(), InputValidationError)

    @inlineCallbacks
    def test_put_update_node_languages_removing_en_adding_fr(self):
        # this tests start setting en as the only enabled language and
        # ends keeping enabled only french.
        self.dummyNode['languages_enabled'] = ["en"]
        self.dummyNode['default_language'] = "en"
        handler = self.request(self.dummyNode, role='admin')
        yield handler.put()

        self.dummyNode['languages_enabled'] = ["fr"]
        self.dummyNode['default_language'] = "fr"
        handler = self.request(self.dummyNode, role='admin')
        yield handler.put()

    @inlineCallbacks
    def test_update_ignored_fields(self):
        self.dummyNode['onionservice'] = 'xxx'
        self.dummyNode['hostname'] = 'yyy'

        handler = self.request(self.dummyNode, role='admin')

        resp = yield handler.put()

        self.assertNotEqual('xxx', resp['hostname'])
        self.assertNotEqual('yyy', resp['onionservice'])

    @inlineCallbacks
    def test_receiver_update_field(self):
        '''Confirm fields out of the receiver's set updates are ignored'''

        self.dummyNode['header_title_submissionpage'] = "Whisteblowing FTW"

        handler = self.request(self.dummyNode, role='receiver')
        resp = yield handler.put()
        self.assertEqual("Whisteblowing FTW", resp['header_title_submissionpage'])