# -*- coding: utf-8 -*-
import pytest
from mock import patch
import sys
import payplug
from payplug import exceptions, notifications
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestTreatNotificationsIssue(TestBase):
    @classmethod
    def setup_class(cls):
        cls.patcher_http_client = patch('payplug.resources.HttpClient')
        cls.patcher_http_client.start()

    @classmethod
    def teardown_class(cls):
        cls.patcher_http_client.stop()

    def test_treat_invalid_json(self):
        with pytest.raises(exceptions.UnknownAPIResource) as excinfo:
            notifications.treat('"malformed JSON')
        assert str(excinfo.value) == 'Request body is malformed JSON.'

    def test_treat_unknown_api_resource(self):
        with pytest.raises(exceptions.UnknownAPIResource):
            notifications.treat('{"id": "payment_id", "object": "bouillabaisse"}')

    def test_treat_invalide_api_resource(self):
        with pytest.raises(exceptions.UnknownAPIResource) as excinfo:
            notifications.treat('{"this_resource": "has_no_id", "object": "payment"}')
        assert str(excinfo.value) == 'The API resource provided is invalid.'


@patch('payplug.config.secret_key', 'a_secret_key')
class TestTreatNotificationsSuccess(TestBase):
    @classmethod
    def setup_class(cls):
        api_response = {
            "id": "pay_test",
            "object": "payment",
        }
        cls.patcher_get = patch.object(payplug.resources.HttpClient, 'get', return_value=(api_response, 200))
        cls.patcher_get.start()

    @classmethod
    def teardown_class(cls):
        cls.patcher_get.stop()

    def test_treat_payment(self):
        safe_payment = notifications.treat('{"id": "pay_test_unsafe", "object": "payment"}')
        assert safe_payment.id == 'pay_test'

    @pytest.mark.skipif(sys.version_info < (3, 0), reason='Binary type in Python3 only.')
    def test_treat_binary_string(self):
        safe_payment = notifications.treat(b'{"id": "pay_test_unsafe", "object": "payment"}')
        assert safe_payment.id == 'pay_test'
