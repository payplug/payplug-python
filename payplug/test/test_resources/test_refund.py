# -*- coding: utf-8 -*-
import pytest
from mock import patch
import payplug
from payplug.resources import Refund
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestRefundResource(TestBase):
    def test_initialize_refund(self):
        refund_attributes = {
            "id": "re_3NxGqPfSGMHQgLSZH0Mv3B",
            "object": "refund",
            "created_at": 1434012358,
            "payment_id": "pay_5iHMDxy4ABR4YBVW4UscIn",
            "amount": 358,
            "currency": "EUR",
            "is_live": True,
            "metadata": {
                "customer_id": 42710,
                "reason": "The delivery was delayed"
            },
        }

        refund_object = Refund(**refund_attributes)

        assert refund_object.id == "re_3NxGqPfSGMHQgLSZH0Mv3B"
        assert refund_object.object == "refund"
        assert refund_object.created_at == 1434012358
        assert refund_object.payment_id == "pay_5iHMDxy4ABR4YBVW4UscIn"
        assert refund_object.amount == 358
        assert refund_object.currency == "EUR"
        assert refund_object.is_live is True
        assert isinstance(refund_object.metadata, dict)
        assert refund_object.metadata['customer_id'] == 42710
        assert refund_object.metadata['reason'] == "The delivery was delayed"


@pytest.fixture
def refund_fixture():
    return {
        "id": "re_5iHMDxy4ABR4YBVW4UscIn",
        "payment_id": "pay_3fJie31HD5eF3dAjdI3903",
        "object": "refund",
    }


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: (refund_fixture(), 200))
class TestConsistentRefund(TestBase):
    @patch('payplug.resources.routes.url')
    def test_get_consistent_resource(self, routes_url_mock):
        unsafe_refund = Refund(id='re_5iHMDxy4ABR4YBVW4UscIn_unsafe',
                               payment_id='pay_3fJie31HD5eF3dAjdI3903_unsafe',
                               object='refund')
        safe_refund = unsafe_refund.get_consistent_resource()

        assert isinstance(safe_refund, Refund)
        assert routes_url_mock.call_args[1]['resource_id'] == 're_5iHMDxy4ABR4YBVW4UscIn_unsafe'
        assert routes_url_mock.call_args[1]['payment_id'] == 'pay_3fJie31HD5eF3dAjdI3903_unsafe'
        assert safe_refund.id == 're_5iHMDxy4ABR4YBVW4UscIn'
        assert safe_refund.payment_id == 'pay_3fJie31HD5eF3dAjdI3903'
