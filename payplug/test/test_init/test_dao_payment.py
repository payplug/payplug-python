# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestPaymentCreateRetrieve(TestBase):
    @classmethod
    def setup_class(cls):
        cls.patcher_post = patch.object(payplug.HttpClient, 'post', return_value=({'id': 'pay_payment_id'}, 200))
        cls.patcher_get = patch.object(payplug.HttpClient, 'get', return_value=({'id': 'pay_payment_id'}, 200))
        cls.patcher_post.start()
        cls.patcher_get.start()

    @classmethod
    def teardown_class(cls):
        cls.patcher_post.stop()
        cls.patcher_get.stop()

    def test_retrieve(self):
        payment = payplug.Payment.retrieve('pay_payment_id')

        assert isinstance(payment, resources.Payment)
        assert payment.id == 'pay_payment_id'

    def test_create(self):
        payment = payplug.Payment.create(some='payment', da='ta')

        assert isinstance(payment, resources.Payment)
        assert payment.id == 'pay_payment_id'


@patch('payplug.config.secret_key', 'a_secret_key')
class TestPaymentList(TestBase):
    @classmethod
    def setup_class(cls):
        api_response = {
            "type": "list",
            "page": 0,
            "per_page": 10,
            "count": 2,
            "data": [
                {
                    "id": "pay_5iHMDxy4ABR4YBVW4UscIn",
                    "object": "payment",
                }
            ]
        }
        cls.patcher_get = patch.object(payplug.HttpClient, 'get', return_value=(api_response, 200))
        cls.patcher_get.start()

    @classmethod
    def teardown_class(cls):
        cls.patcher_get.stop()

    @patch('payplug.routes.url')
    def test_list_pagination_no_arguments(self, url_mock):
        payplug.Payment.list()
        assert url_mock.call_args[0][1] == {}

    @patch('payplug.routes.url')
    def test_list_pagination_page_argument(self, url_mock):
        payplug.Payment.list(page=1)
        assert url_mock.call_args[0][1] == {'page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_per_page_argument(self, url_mock):
        payplug.Payment.list(per_page=1)
        assert url_mock.call_args[0][1] == {'per_page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_page_and_per_page_arguments(self, url_mock):
        payplug.Payment.list(page=42, per_page=1)
        assert url_mock.call_args[0][1] == {'page': 42, 'per_page': 1}

    def test_list(self):
        payments = payplug.Payment.list()

        assert isinstance(payments, resources.APIResourceCollection)
        assert next(payments).id == 'pay_5iHMDxy4ABR4YBVW4UscIn'
