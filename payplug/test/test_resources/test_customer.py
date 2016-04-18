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
