# -*- coding: utf-8 -*-
from mock import patch
from payplug.resources import Customer
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestCustomerResource(TestBase):
    def test_initialize_customer(self):
        customer_attributes = {
            "id": "cus_6ESfofiMiLBjC6",
            "object": "customer",
            "created_at": 1434010787,
            "is_live": True,
            "email": "john.watson@example.net",
            "first_name": "John",
            "last_name": "Watson",
            "address1": "27 Rue Pasteur",
            "address2": None,
            "city": "Paris",
            "postcode": "75018",
            "country": "France",
            "metadata": {
                "customer_id": 42710,
                "customer_name": "Jean",
            },
        }

        customer = Customer(**customer_attributes)

        assert customer.id == "cus_6ESfofiMiLBjC6"
        assert customer.object == "customer"
        assert customer.created_at == 1434010787
        assert customer.is_live is True
        assert customer.email == "john.watson@example.net"
        assert customer.first_name == "John"
        assert customer.last_name == "Watson"
        assert customer.address1 == "27 Rue Pasteur"
        assert customer.address2 is None
        assert customer.city == "Paris"
        assert customer.postcode == "75018"
        assert customer.country == "France"

        assert isinstance(customer.metadata, dict)
        assert customer.metadata["customer_id"] == 42710
        assert customer.metadata["customer_name"] == "Jean"

    @patch('payplug.resources.payplug.Customer.update')
    def test_update_payment(self, customer_update_mock):
        customer = Customer(id='cus_customer1')
        customer.update(da='ta')
        customer_update_mock.assert_called_once_with(customer, da='ta')

    @patch('payplug.resources.payplug.Card.create')
    def test_add_card(self, card_create_mock):
        customer = Customer(id='cus_customer1')
        customer.add_card(some='data')
        card_create_mock.assert_called_once_with(customer, some='data')

    @patch('payplug.resources.payplug.Card.list')
    def test_list_cards(self, card_list_mock):
        customer = Customer(id='cus_customer1')
        customer.list_cards(per_page=10, page=0)
        card_list_mock.assert_called_once_with(customer, per_page=10, page=0)
