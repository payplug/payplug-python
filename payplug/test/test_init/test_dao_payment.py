# -*- coding: utf-8 -*-
import pytest
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'post', lambda *args, **kwargs: ({'id': 'pay_payment_id'}, 201))
@patch.object(payplug.HttpClient, 'patch', lambda *args, **kwargs: ({'id': 'pay_payment_id'}, 200))
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: ({'id': 'pay_payment_id'}, 200))
class TestPaymentCreateRetrieveAbort(TestBase):
    def test_retrieve(self):
        payment = payplug.Payment.retrieve('pay_payment_id')

        assert isinstance(payment, resources.Payment)
        assert payment.id == 'pay_payment_id'

    def test_abort(self):
        payment = payplug.Payment.abort('pay_payment_id')

        assert isinstance(payment, resources.Payment)
        assert payment.id == 'pay_payment_id'

    def test_abort_with_payment_object(self):
        payment = payplug.Payment.retrieve('pay_payment_id')
        payment = payplug.Payment.abort(payment)

        assert isinstance(payment, resources.Payment)
        assert payment.id == 'pay_payment_id'

    def test_create(self):
        payment = payplug.Payment.create(some='payment', da='ta')

        assert isinstance(payment, resources.Payment)
        assert payment.id == 'pay_payment_id'


def get_payments_fixture():
    return {
        "type": "list",
        "page": 0,
        "per_page": 10,
        "count": 2,
        "data": [
            {
                "id": "pay_5iHMDxy4ABR4YBVW4UscIn",
                "object": "payment",
            },
        ]
    }


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: (get_payments_fixture(), 200))
class TestPaymentList(TestBase):
    @patch('payplug.routes.url')
    def test_list_pagination_no_arguments(self, url_mock):
        payplug.Payment.list()
        assert url_mock.call_args[1]['pagination'] == {}

    @patch('payplug.routes.url')
    def test_list_pagination_page_argument(self, url_mock):
        payplug.Payment.list(page=1)
        assert url_mock.call_args[1]['pagination'] == {'page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_per_page_argument(self, url_mock):
        payplug.Payment.list(per_page=1)
        assert url_mock.call_args[1]['pagination'] == {'per_page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_page_and_per_page_arguments(self, url_mock):
        payplug.Payment.list(page=42, per_page=1)
        assert url_mock.call_args[1]['pagination'] == {'page': 42, 'per_page': 1}

    def test_list(self):
        payments = payplug.Payment.list()

        assert isinstance(payments, resources.APIResourceCollection)
        assert next(payments).id == 'pay_5iHMDxy4ABR4YBVW4UscIn'
