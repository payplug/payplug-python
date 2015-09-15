# -*- coding: utf-8 -*-
import pytest
from payplug.resources import APIResourceCollection, Payment
from payplug.test import TestBase


class TestAPIResourceCollection(TestBase):
    @pytest.fixture(scope='class')
    def api_response(self):
        return {
            "type": "list",
            "page": 0,
            "per_page": 10,
            "count": 46,
            "data": [
                {
                    "id": "pay_5iHMDxy4ABR4YBVW4UscIn",
                    "object": "payment",
                    "is_live": True,
                    "amount": 3300
                },
                {
                    "id": "pay_3uFHHU3949uUF2A98s0CqE",
                    "object": "payment",
                    "is_live": False,
                    "amount": 44012
                },
            ]
        }

    def test_resource_collection(self, api_response):
        resource = APIResourceCollection(Payment, **api_response)

        assert resource.type == "list"
        assert resource.page == 0
        assert resource.per_page == 10
        assert resource.count == 46

        assert type(resource.data) == list
        assert len(resource.data) == 2
        assert all([isinstance(p, Payment) for p in resource.data])

        assert resource.data[0].id == "pay_5iHMDxy4ABR4YBVW4UscIn"
        assert resource.data[0].object == "payment"
        assert resource.data[0].is_live is True
        assert resource.data[0].amount == 3300

        assert resource.data[1].id == "pay_3uFHHU3949uUF2A98s0CqE"
        assert resource.data[1].object == "payment"
        assert resource.data[1].is_live is False
        assert resource.data[1].amount == 44012

    def test_iterate(self, api_response):
        resource = APIResourceCollection(Payment, **api_response)

        r = next(resource)
        assert isinstance(r, Payment)
        assert r.id == "pay_5iHMDxy4ABR4YBVW4UscIn"

        r = next(resource)
        assert isinstance(r, Payment)
        assert r.id == "pay_3uFHHU3949uUF2A98s0CqE"

        with pytest.raises(StopIteration):
            next(resource)

    def test_iter(self, api_response):
        resource = APIResourceCollection(Payment, **api_response)
        for payment in iter(resource):
            assert isinstance(payment, Payment)
