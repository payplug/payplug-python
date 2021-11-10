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

    def test_treat_invalid_api_resource(self):
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


@patch('payplug.config.secret_key', 'a_secret_key')
class TestTreatNotificationsInstallmentPlanSuccess(TestBase):
    @classmethod
    def setup_class(cls):
        api_response = {
            "hosted_payment": {
                "cancel_url": "https://example.com/payment/payplug/cancel",
                "return_url": "https://example.com/shop/payment/validate",
                "payment_url": "https://secure.payplug.com/pay/test/59TXrYROSdmt0Y7W9Ubpg8"
            },
            "customer": {
                "phone_number": "None",
                "city": "PARIS",
                "first_name": "JOHN",
                "last_name": "DOE",
                "language": "fr",
                "address1": "21 Elm Street",
                "address2": "None",
                "postcode": "75018",
                "country": "France",
                "email": "johndoe@example.com",
            },
            "schedule": [
                {"date": "2021-08-04", "amount": 2600, "payment_ids": ["pay_59TXrYROSdmt0Y7W9Ubpg8"]},
                {"date": "2021-09-04", "amount": 2600, "payment_ids": []},
                {"date": "2021-10-04", "amount": 2600, "payment_ids": []},
            ],
            "notification": {"url": "https://example.com/payment/payplug/ipn"},
            "created_at": 1628079236,
            "object": "installment_plan",
            "is_active": True,
            "currency": "EUR",
            "is_live": False,
            "is_fully_paid": False,
            "id": "inst_2aSCmLRZFtAA7arHJfGrE1",
            "failure": "None",
            "metadata": {"customer_id": "23", "acquirer_id": 5, "reference": "CMD0000123"},
        }
        cls.patcher_get = patch.object(payplug.resources.HttpClient, 'get', return_value=(api_response, 200))
        cls.patcher_get.start()

    @classmethod
    def teardown_class(cls):
        cls.patcher_get.stop()

    def test_treat_installment_plan(self):
        json_data = '''{
            "hosted_payment":{
                "cancel_url":"https://example.com/payment/payplug/cancel",
                "return_url":"https://example.com/shop/payment/validate",
                "payment_url":"https://secure.payplug.com/pay/test/59TXrYROSdmt0Y7W9Ubpg8"
            },
            "customer":{
                "phone_number":"None",
                "city":"PARIS",
                "first_name":"JOHN",
                "last_name":"DOE",
                "language":"fr",
                "address1":"21 Elm Street",
                "address2":"None",
                "postcode":"75018",
                "country":"France",
                "email":"johndoe@example.com"
            },
            "schedule":[
                {
                    "date":"2021-08-04",
                    "amount":2600,
                    "payment_ids":[
                        "pay_59TXrYROSdmt0Y7W9Ubpg8"
                    ]
                },
                {
                    "date":"2021-09-04",
                    "amount":2600,
                    "payment_ids":[
                        
                    ]
                },
                {
                    "date":"2021-10-04",
                    "amount":2600,
                    "payment_ids":[
                        
                    ]
                }
            ],
            "notification":{
                "url":"https://example.com/payment/payplug/ipn"
            },
            "created_at":1628079236,
            "object":"installment_plan",
            "is_active":true,
            "currency":"EUR",
            "is_live":false,
            "is_fully_paid":false,
            "id":"inst_2aSCmLRZFtAA7arHJfGrE1",
            "failure":"None",
            "metadata":{
                "customer_id":"23",
                "acquirer_id":5,
                "reference":"CMD0000123"
            }
        }'''
        safe_installment_plan = notifications.treat(json_data)
        assert safe_installment_plan.id == 'inst_2aSCmLRZFtAA7arHJfGrE1'
