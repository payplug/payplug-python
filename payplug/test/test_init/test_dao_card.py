# -*- coding: utf-8 -*-
import pytest
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'post', lambda *args, **kwargs: ({'id': 'card_card1'}, 201))
@patch.object(payplug.HttpClient, 'patch', lambda *args, **kwargs: ({'id': 'card_card1'}, 200))
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: ({'id': 'card_card1'}, 200))
@patch.object(payplug.HttpClient, 'delete', lambda *args, **kwargs: ({}, 204))
class TestCardCreateRetrieveDelete(TestBase):
    @pytest.fixture
    def customer_fixture(self):
        return resources.Customer(id='cus_customer1')

    def test_retrieve(self):
        card = payplug.Card.retrieve('cus_customer1', 'card_card1')

        assert isinstance(card, resources.Card)
        assert card.id == 'card_card1'

    def test_retrieve_with_customer_object(self, customer_fixture):
        card = payplug.Card.retrieve(customer_fixture, 'card_card1')

        assert isinstance(card, resources.Card)
        assert card.id == 'card_card1'

    def test_create(self):
        card = payplug.Card.create('cus_customer1', some='card', da='ta')

        assert isinstance(card, resources.Card)
        assert card.id == 'card_card1'

    def test_create_with_customer_object(self, customer_fixture):
        card = payplug.Card.create(customer_fixture, some='card', da='ta')

        assert isinstance(card, resources.Card)
        assert card.id == 'card_card1'

    def test_delete(self):
        res = payplug.Card.delete('cus_customer1', 'card_card1')

        assert res is None

    def test_delete_with_customer_object(self, customer_fixture):
        res = payplug.Card.delete(customer_fixture, 'card_card1')

        assert res is None

    def test_delete_with_card_object(self):
        card = resources.Card(id='card_card1')
        res = payplug.Card.delete('cus_customer1', card)

        assert res is None


@pytest.fixture
def cards_list_fixture():
    return {
        "type": "list",
        "page": 0,
        "per_page": 10,
        "count": 2,
        "data": [
            {
                "id": "card_card1",
                "object": "card",
            },
            {
                "id": "card_card2",
                "object": "card",
            },
        ]
    }


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: (cards_list_fixture(), 200))
class TestCardsList(TestBase):
    @pytest.fixture
    def customer_fixture(self):
        return resources.Customer(id='cus_customer1')

    @patch('payplug.routes.url')
    def test_list_pagination_no_arguments(self, url_mock, customer_fixture):
        payplug.Card.list(customer_fixture)
        assert url_mock.call_args[1]['pagination'] == {}

    @patch('payplug.routes.url')
    def test_list_pagination_page_argument(self, url_mock, customer_fixture):
        payplug.Card.list(customer_fixture, page=1)
        assert url_mock.call_args[1]['pagination'] == {'page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_per_page_argument(self, url_mock, customer_fixture):
        payplug.Card.list(customer_fixture, per_page=1)
        assert url_mock.call_args[1]['pagination'] == {'per_page': 1}

    @patch('payplug.routes.url')
    def test_list_pagination_page_and_per_page_arguments(self, url_mock, customer_fixture):
        payplug.Card.list(customer_fixture, page=42, per_page=1)
        assert url_mock.call_args[1]['pagination'] == {'page': 42, 'per_page': 1}

    def test_list(self, customer_fixture):
        cards = payplug.Card.list(customer_fixture)

        assert isinstance(cards, resources.APIResourceCollection)
        assert next(cards).id == 'card_card1'
        assert next(cards).id == 'card_card2'
