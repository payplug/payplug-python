# -*- coding: utf-8 -*-
import pytest
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'post', lambda *args, **kwargs: ({'id': 'cus_customer_id'}, 201))
@patch.object(payplug.HttpClient, 'patch', lambda *args, **kwargs: ({'id': 'cus_customer_id'}, 200))
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: ({'id': 'cus_customer_id'}, 200))
@patch.object(payplug.HttpClient, 'delete', lambda *args, **kwargs: ({}, 204))
class TestCustomerCreateRetrieveUpdateDelete(TestBase):
    def test_retrieve(self):
        customer = payplug.Customer.retrieve('cus_customer_id')

        assert isinstance(customer, resources.Customer)
        assert customer.id == 'cus_customer_id'

    def test_update(self):
        customer = payplug.Customer.update('cus_customer_id', some='data')

        assert isinstance(customer, resources.Customer)
        assert customer.id == 'cus_customer_id'

    def test_update_with_customer_object(self):
        customer = payplug.Customer.retrieve('cus_customer_id')
        customer = payplug.Customer.update(customer, some='data')

        assert isinstance(customer, resources.Customer)
        assert customer.id == 'cus_customer_id'

    def test_create(self):
        customer = payplug.Customer.create(some='customer', da='ta')

        assert isinstance(customer, resources.Customer)
        assert customer.id == 'cus_customer_id'

    def test_delete(self):
        res = payplug.Customer.delete('cus_customer_id')

        assert res is None

    def test_delete_with_customer_object(self):
        customer = payplug.Customer.retrieve('cus_customer_id')
        res = payplug.Customer.delete(customer)

        assert res is None


def customers_list_fixture():
    return {
        "type": "list",
        "page": 0,
        "per_page": 10,
        "count": 2,
        "data": [
            {
                "id": "cus_customer1",
                "object": "customer",
            },
            {
                "id": "cus_customer2",
                "object": "customer",
            },
        ]
    }


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: (customers_list_fixture(), 200))
class TestCustomerList(TestBase):
    @patch('payplug.routes.url')
    def test_list_pagination_no_arguments(self, url_mock):
        payplug.Customer.list()
        assert url_mock.call_args[1]['pagination'] == {}

    @patch('payplug.routes.url')
    def test_list_pagination_page_argument(self, url_mock):
        payplug.Customer.list(page=1)
        assert url_mock.call_args[1]['pagination'] == {'page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_per_page_argument(self, url_mock):
        payplug.Customer.list(per_page=1)
        assert url_mock.call_args[1]['pagination'] == {'per_page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_page_and_per_page_arguments(self, url_mock):
        payplug.Customer.list(page=42, per_page=1)
        assert url_mock.call_args[1]['pagination'] == {'page': 42, 'per_page': 1}

    def test_list(self):
        customers = payplug.Customer.list()

        assert isinstance(customers, resources.APIResourceCollection)
        assert next(customers).id == 'cus_customer1'
        assert next(customers).id == 'cus_customer2'
