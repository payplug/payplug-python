# -*- coding: utf-8 -*-
import pytest
from payplug import exceptions, resources
from payplug.resources import APIResource
from payplug.test import TestBase


class TestAPIResource(TestBase):
    def test_get_attribute(self):
        resource = APIResource(foo='bar', val=22)
        assert resource.foo == 'bar'
        assert resource.val == 22
        assert resource._attributes == {'foo': 'bar', 'val': 22}

    def test_get_undefined_attribute(self):
        resource = APIResource(foo='bar', val=22)
        with pytest.raises(AttributeError) as excinfo:
            resource.baz
        assert '`baz`' in str(excinfo.value)

    def test_set_attributes_manually(self):
        resource = APIResource(foo='bar')
        resource.bar = 'baz'
        assert resource.bar == 'baz'
        assert not hasattr(resource, 'baz')

    def test_factory_without_object_key(self):
        with pytest.raises(exceptions.UnknownAPIResource) as excinfo:
            APIResource.factory({'id': 'no_object_key'})
        assert str(excinfo.value) == 'Missing `object` key in resource.'

    def test_factory_with_payment(self):
        payment = APIResource.factory({'id': 'a_payment_id', 'object': 'payment'})
        assert isinstance(payment, resources.Payment)
        assert payment.id == 'a_payment_id'
        assert payment.object == 'payment'

    def test_factory_with_refund(self):
        refund = APIResource.factory({'id': 'a_refund_id', 'object': 'refund'})
        assert isinstance(refund, resources.Refund)
        assert refund.id == 'a_refund_id'
        assert refund.object == 'refund'

    def test_with_unknown_object(self):
        with pytest.raises(exceptions.UnknownAPIResource) as excinfo:
            APIResource.factory({'id': 'boo_42', 'object': 'bouillabaisse'})
        assert str(excinfo.value) == 'Unknown object `bouillabaisse`.'
