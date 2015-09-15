# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestRefundCreateRetrieve(TestBase):
    @classmethod
    def setup_class(cls):
        cls.patcher_post = patch.object(payplug.HttpClient, 'post', return_value=({'id': 're_refund_id'}, 200))
        cls.patcher_get = patch.object(payplug.HttpClient, 'get', return_value=({'id': 're_refund_id'}, 200))
        cls.patcher_post.start()
        cls.patcher_get.start()

    @classmethod
    def teardown_class(cls):
        cls.patcher_post.stop()
        cls.patcher_get.stop()

    @patch('payplug.routes.url')
    def test_retrieve_with_payment_id(self, url_mock):
        refund = payplug.Refund.retrieve('pay_payment_id', 're_refund_id')

        assert url_mock.call_args[1]['payment_id'] == 'pay_payment_id'
        assert url_mock.call_args[1]['refund_id'] == 're_refund_id'

        assert isinstance(refund, resources.Refund)

    @patch('payplug.routes.url')
    def test_retrieve_with_payment_object(self, url_mock):
        payment = resources.Payment(id='pay_payment_id')
        refund = payplug.Refund.retrieve(payment, 're_refund_id')

        assert url_mock.call_args[1]['payment_id'] == 'pay_payment_id'
        assert url_mock.call_args[1]['refund_id'] == 're_refund_id'

        assert isinstance(refund, resources.Refund)

    @patch('payplug.routes.url')
    def test_create_with_payment_id(self, url_mock):
        refund = payplug.Refund.create('pay_payment_id', da='ta')

        assert url_mock.call_args[1]['payment_id'] == 'pay_payment_id'

        assert isinstance(refund, resources.Refund)

    @patch('payplug.routes.url')
    def test_create_with_payment_object(self, url_mock):
        payment = resources.Payment(id='pay_payment_id')
        refund = payplug.Refund.create(payment, da='ta')

        assert url_mock.call_args[1]['payment_id'] == 'pay_payment_id'

        assert isinstance(refund, resources.Refund)


@patch('payplug.config.secret_key', 'a_secret_key')
class TestRefundList(TestBase):
    @classmethod
    def setup_class(cls):
        api_response = {
            "type": "list",
            "data": [
                {
                    "id": "re_3NxGqPfSGMHQgLSZH0Mv3B",
                    "payment_id": "pay_5iHMDxy4ABR4YBVW4UscIn",
                    "object": "refund",
                    "is_live": True,
                    "amount": 358,
                    "currency": "EUR",
                    "created_at": 1434012358,
                    "metadata": {
                        "customer_id": 42710,
                        "reason": "The delivery was delayed"
                    }
                }
            ]
        }
        cls.patcher_get = patch.object(payplug.HttpClient, 'get', return_value=(api_response, 200))
        cls.patcher_get.start()

    @classmethod
    def teardown_class(cls):
        cls.patcher_get.stop()

    @patch('payplug.routes.url')
    def test_list_with_payment_id(self, url_mock):
        refunds = payplug.Refund.list('pay_payment_id')

        assert url_mock.call_args[1]['payment_id'] == 'pay_payment_id'

        assert isinstance(refunds, resources.APIResourceCollection)
        assert next(refunds).id == 're_3NxGqPfSGMHQgLSZH0Mv3B'

    @patch('payplug.routes.url')
    def test_list_with_payment_object(self, url_mock):
        payment = resources.Payment(id='pay_payment_id')
        refunds = payplug.Refund.list(payment)

        assert url_mock.call_args[1]['payment_id'] == 'pay_payment_id'

        assert isinstance(refunds, resources.APIResourceCollection)
        assert next(refunds).id == 're_3NxGqPfSGMHQgLSZH0Mv3B'
