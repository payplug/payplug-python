# -*- coding: utf-8 -*-
from mock import patch
from payplug.resources import Card
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestCardResource(TestBase):
    def test_initialize_card(self):
        card_attributes = {
            "id": "card_167oJVCpvtR9j8N85LraL2GA",
            "object": "card",
            "customer_id": "cus_6ESfofiMiLBjC6",
            "created_at": 1434010787,
            "last4": "1111",
            "brand": "visa",
            "exp_moth": 5,
            "exp_year": 2019,
            "country": "FR",
            "metadata": {
                "customer_id": 42710,
                "customer_name": "Jean",
            },
        }

        card = Card(**card_attributes)

        assert card.id == "card_167oJVCpvtR9j8N85LraL2GA"
        assert card.object == "card"
        assert card.customer_id == "cus_6ESfofiMiLBjC6"
        assert card.created_at == 1434010787
        assert card.last4 == "1111"
        assert card.brand == "visa"
        assert card.exp_moth == 5
        assert card.exp_year == 2019
        assert card.country == "FR"

        assert isinstance(card.metadata, dict)
        assert card.metadata["customer_id"] == 42710
        assert card.metadata["customer_name"] == "Jean"
