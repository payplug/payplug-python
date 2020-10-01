# -*- coding: utf-8 -*-
import pytest
from mock import patch
import payplug
from payplug.resources import Payment
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestPaymentResource(TestBase):
    def test_initialize_payment_old(self):
        payment_attributes = {
            "id": "pay_5iHMDxy4ABR4YBVW4UscIn",
            "object": "payment",
            "is_live": True,
            "amount": 3300,
            "amount_refunded": 0,
            "currency": "EUR",
            "created_at": 1434010787,
            "is_paid": True,
            "is_refunded": False,
            "is_3ds": False,
            "save_card": False,
            "card": {
                "last4": "1800",
                "country": "FR",
                "exp_month": 9,
                "exp_year": 2017,
                "brand": "Mastercard"
            },
            "customer": {
                "first_name": "John",
                "last_name": "Watson",
                "email": "john.watson@example.net",
                "address1": None,
                "address2": None,
                "postcode": None,
                "city": None,
                "country": None
            },
            "hosted_payment": {
                "payment_url": "hosted_payment_payment_url",
                "return_url": "hosted_payment_return_url",
                "cancel_url": "hosted_payment_cancel_url",
                "paid_at": 1434010827
            },
            "notification": {
                "url": "notification_url",
                "response_code": 200
            },
            "failure": {
                "code": "a_failure_code",
                "message": 'A weird failure message ®±'
            },
            "metadata": {
                "customer_id": 42710
            }
        }

        payment = Payment(**payment_attributes)

        assert payment.id == 'pay_5iHMDxy4ABR4YBVW4UscIn'
        assert payment.object == 'payment'
        assert payment.is_live is True
        assert payment.amount == 3300
        assert payment.amount_refunded == 0
        assert payment.currency == "EUR"
        assert payment.created_at == 1434010787
        assert payment.is_paid is True
        assert payment.is_refunded is False
        assert payment.is_3ds is False
        assert payment.save_card is False

        assert type(payment.card) == Payment.Card
        assert payment.card.last4 == "1800"
        assert payment.card.country == "FR"
        assert payment.card.exp_month == 9
        assert payment.card.exp_year == 2017
        assert payment.card.brand == "Mastercard"

        assert type(payment.customer) == Payment.Customer
        assert payment.customer.first_name == "John"
        assert payment.customer.last_name == "Watson"
        assert payment.customer.email == "john.watson@example.net"
        assert payment.customer.address1 is None
        assert payment.customer.address2 is None
        assert payment.customer.postcode is None
        assert payment.customer.city is None
        assert payment.customer.country is None

        assert type(payment.hosted_payment) == Payment.HostedPayment
        assert payment.hosted_payment.payment_url == "hosted_payment_payment_url"
        assert payment.hosted_payment.return_url == "hosted_payment_return_url"
        assert payment.hosted_payment.cancel_url == "hosted_payment_cancel_url"
        assert payment.hosted_payment.paid_at == 1434010827

        assert type(payment.notification) == Payment.Notification
        assert payment.notification.url == "notification_url"
        assert payment.notification.response_code == 200

        assert type(payment.failure) == Payment.Failure
        assert payment.failure.code == "a_failure_code"
        assert payment.failure.message == 'A weird failure message ®±'

        assert isinstance(payment.metadata, dict)
        assert payment.metadata['customer_id'] == 42710

    def test_initialize_payment_2019(self):
        payment_attributes = {
            "id": "pay_5iHMDxy4ABR4YBVW4UscIn",
            "object": "payment",
            "is_live": True,
            "amount": 3300,
            "amount_refunded": 0,
            "currency": "EUR",
            "created_at": 1434010787,
            "is_paid": True,
            "is_refunded": False,
            "is_3ds": False,
            "save_card": False,
            "card": {
                "last4": "1800",
                "country": "FR",
                "exp_month": 9,
                "exp_year": 2017,
                "brand": "Mastercard"
            },
            "hosted_payment": {
                "payment_url": "hosted_payment_payment_url",
                "return_url": "hosted_payment_return_url",
                "cancel_url": "hosted_payment_cancel_url",
                "paid_at": 1434010827
            },
            "notification": {
                "url": "notification_url",
                "response_code": 200
            },
            "failure": {
                "code": "a_failure_code",
                "message": 'A weird failure message ®±'
            },
            "metadata": {
                "customer_id": 42710
            },
            'billing': {
                'title': 'mr',
                'first_name': 'John',
                'last_name': 'Watson',
                'email': 'john.watson@example.net',
                'address1': '221B Baker Street',
                'postcode': 'NW16XE',
                'city': 'London',
                'country': 'GB',
                'language': 'en'
            },
            'shipping': {
                'title': 'mr',
                'first_name': 'John',
                'last_name': 'Watson',
                'email': 'john.watson@example.net',
                'address1': '221B Baker Street',
                'postcode': 'NW16XE',
                'city': 'London',
                'country': 'GB',
                'language': 'en',
                'delivery_type': 'BILLING'
            },
        }

        payment = Payment(**payment_attributes)

        assert payment.id == 'pay_5iHMDxy4ABR4YBVW4UscIn'
        assert payment.object == 'payment'
        assert payment.is_live is True
        assert payment.amount == 3300
        assert payment.amount_refunded == 0
        assert payment.currency == "EUR"
        assert payment.created_at == 1434010787
        assert payment.is_paid is True
        assert payment.is_refunded is False
        assert payment.is_3ds is False
        assert payment.save_card is False

        assert type(payment.card) == Payment.Card
        assert payment.card.last4 == "1800"
        assert payment.card.country == "FR"
        assert payment.card.exp_month == 9
        assert payment.card.exp_year == 2017
        assert payment.card.brand == "Mastercard"

        assert type(payment.billing) == Payment.Billing
        assert payment.billing.title == 'mr'
        assert payment.billing.first_name == "John"
        assert payment.billing.last_name == "Watson"
        assert payment.billing.email == "john.watson@example.net"
        assert payment.billing.address1 == '221B Baker Street'
        assert payment.billing.postcode == 'NW16XE'
        assert payment.billing.city == 'London'
        assert payment.billing.country == 'GB'
        assert payment.billing.language == 'en'

        assert type(payment.shipping) == Payment.Shipping
        assert payment.shipping.title == 'mr'
        assert payment.shipping.first_name == "John"
        assert payment.shipping.last_name == "Watson"
        assert payment.shipping.email == "john.watson@example.net"
        assert payment.shipping.address1 == '221B Baker Street'
        assert payment.shipping.postcode == 'NW16XE'
        assert payment.shipping.city == 'London'
        assert payment.shipping.country == 'GB'
        assert payment.shipping.language == 'en'
        assert payment.shipping.delivery_type == 'BILLING'

        assert type(payment.hosted_payment) == Payment.HostedPayment
        assert payment.hosted_payment.payment_url == "hosted_payment_payment_url"
        assert payment.hosted_payment.return_url == "hosted_payment_return_url"
        assert payment.hosted_payment.cancel_url == "hosted_payment_cancel_url"
        assert payment.hosted_payment.paid_at == 1434010827

        assert type(payment.notification) == Payment.Notification
        assert payment.notification.url == "notification_url"
        assert payment.notification.response_code == 200

        assert type(payment.failure) == Payment.Failure
        assert payment.failure.code == "a_failure_code"
        assert payment.failure.message == 'A weird failure message ®±'

        assert isinstance(payment.metadata, dict)
        assert payment.metadata['customer_id'] == 42710

    @patch('payplug.resources.payplug.Refund.create')
    def test_refund_payment(self, refund_create_mock):
        payment = Payment(id='pay_5iHMDxy4ABR4YBVW4UscIn')
        payment.refund(refund='data')
        refund_create_mock.assert_called_once_with(payment, refund='data')

    @patch('payplug.resources.payplug.Refund.list')
    def test_list_refunds_payment(self, refund_list_mock):
        payment = Payment(id='pay_5iHMDxy4ABR4YBVW4UscIn')
        payment.list_refunds()
        refund_list_mock.assert_called_once_with(payment)

    @patch('payplug.resources.payplug.Payment.abort')
    def test_abort_payment(self, payment_abort_mock):
        payment = Payment(id='pay_5iHMDxy4ABR4YBVW4UscIn')
        payment.abort()
        payment_abort_mock.assert_called_once_with(payment)


def payment_fixture():
    return {
        "id": "pay_5iHMDxy4ABR4YBVW4UscIn",
        "object": "payment",
    }


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: (payment_fixture(), 200))
class TestConsistentPayment(TestBase):
    @patch('payplug.resources.routes.url')
    def test_get_consistent_resource(self, routes_url_mock):
        unsafe_payment = Payment(id='pay_5iHMDxy4ABR4YBVW4UscIn_unsafe', object='payment')
        safe_payment = unsafe_payment.get_consistent_resource()

        assert isinstance(safe_payment, Payment)
        assert routes_url_mock.call_args[1]['resource_id'] == 'pay_5iHMDxy4ABR4YBVW4UscIn_unsafe'
        assert safe_payment.id == 'pay_5iHMDxy4ABR4YBVW4UscIn'
