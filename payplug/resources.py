# -*- coding: utf-8 -*-
import abc
from six import with_metaclass
import payplug
from payplug import exceptions, routes
from payplug.network import HttpClient


class APIResource(with_metaclass(abc.ABCMeta)):
    """
    A simple API resource
    """
    def __init__(self, **resource_attributes):
        """
        :param resource_attributes: API resource parameters
        """
        object.__setattr__(self, '_attributes', {})
        self._initialize(**resource_attributes)

    def __getattr__(self, attribute):
        """
        Read an API resource property.

        :param attribute: the key of the attribute to get
        :type attribute: string

        :return the attribute value
        :rtype mixed

        :raises
            AttributeError when the attribute was not defined for the API resource
        """
        if attribute in self._attributes:
            return self._attributes[attribute]
        raise AttributeError('Unable to find attribute `' + attribute + '`.')

    def __setattr__(self, key, value):
        """
        Set an API resource property.

        :param key: the key to set or the attribute key to set
        :type key: string
        :param value: the value to set or the attribute value
        :type value: mixed
        """
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            self.__dict__['_attributes'][key] = value

    @staticmethod
    def factory(data):
        """
        Try to reconstruct the APIResource from its data.

        :param data: The APIResource data
        :type data: dict

        :return: The guessed APIResource

        :raise
            exceptions.UnkownAPIResource when it's impossible to reconstruct the APIResource from its data.
        """
        if 'object' not in data:
            raise exceptions.UnknownAPIResource('Missing `object` key in resource.')

        for reconstituable_api_resource_type in ReconstituableAPIResource.__subclasses__():
            if reconstituable_api_resource_type.object_type == data['object']:
                return reconstituable_api_resource_type(**data)

        raise exceptions.UnknownAPIResource('Unknown object `' + data['object'] + '`.')

    def _set_attributes(self, **attributes):
        """
        Set the attributes of this resource, possibly removing the old ones if they exist.

        :param attributes: The attributes to set
        """
        self._attributes = attributes

    def _initialize(self, **resource_attributes):
        """
        Initialize a resource.
        Default behavior is just to set all the attributes. You may want to override this.

        :param resource_attributes: The resource attributes
        """
        self._set_attributes(**resource_attributes)
        for attribute, attribute_type in list(self._mapper.items()):
            if attribute in resource_attributes and isinstance(resource_attributes[attribute], dict):
                setattr(self, attribute, attribute_type(**resource_attributes[attribute]))

    @property
    def _mapper(self):
        """
        Maps an attribute name to an APIResource type, so that _initialize method can map this attribute to the given
        type.
        You should override this if you get nested objects in API response.

        :return: A mapping dict
        :rtype: dict(attribute -> type(some class that extends APIResource))
        """
        return {}


class VerifiableAPIResource(with_metaclass(abc.ABCMeta)):
    """
    A verifiable API Resource is an API Resource that can be converted into a consistent object.
    Typically, you need to verify a resource when you received it from a untrustworthy source (e.g. from a notification)
    """
    @abc.abstractmethod
    def get_consistent_resource(self):
        """
        Return an API resource that you can trust

        :return The consistent API Resource
        :rtype APIResource
        """
        pass


class ReconstituableAPIResource(with_metaclass(abc.ABCMeta)):
    """
    A reconstituable API resource can be reconstituted provided only its data.
    """
    @abc.abstractproperty
    def object_type(self):
        """
        Must be static.

        :return The string returned by the API for "object" key.
        """
        pass


class Payment(APIResource, VerifiableAPIResource, ReconstituableAPIResource):
    """
    A payment
    """
    object_type = 'payment'

    @property
    def _mapper(self):
        """
        Maps payment attributes to their specific types.

        :see :func:`~APIResource._mapper`
        """
        return {
            'card': Payment.Card,
            'customer': Payment.Customer,
            'hosted_payment': Payment.HostedPayment,
            'notification': Payment.Notification,
            'failure': Payment.Failure,
        }

    def get_consistent_resource(self):
        """
        :return a payment that you can trust.
        :rtype Payment
        """
        http_client = HttpClient()
        response, _ = http_client.get(routes.url(routes.PAYMENT_RESOURCE, resource_id=self.id))
        return Payment(**response)

    def refund(self, **data):
        """
        Refund a payment directly from the object.

        :param data: the refund data.

        :return The refund object.
        :rtype Refund
        """
        return payplug.Refund.create(self, **data)

    def list_refunds(self):
        """
        List the refunds of a payment.

        :return The refunds iterable object
        :rtype APIResourceCollection
        """
        return payplug.Refund.list(self)

    def abort(self):
        """
        Abort a payment.

        :return The aborted payment object
        :rtype Payment
        """
        return payplug.Payment.abort(self)

    class Card(APIResource):
        """
        A credit card.
        """
        pass

    class Customer(APIResource):
        """
        A customer
        """
        pass

    class HostedPayment(APIResource):
        """
        A hosted payment
        """
        pass

    class Notification(APIResource):
        """
        A notification
        """
        pass

    class Failure(APIResource):
        """
        A payment failure
        """
        pass


class Refund(APIResource, VerifiableAPIResource, ReconstituableAPIResource):
    """
    A Payment refund.
    """
    object_type = 'refund'

    def get_consistent_resource(self):
        """
        :return a refund that you can trust.
        :rtype Refund
        """
        http_client = HttpClient()
        response, _ = http_client.get(
            routes.url(routes.REFUND_RESOURCE, resource_id=self.id, payment_id=self.payment_id)
        )
        return Refund(**response)


class Customer(APIResource, ReconstituableAPIResource):
    """
    A Customer Resource.
    """
    object_type = 'customer'

    def update(self, **data):
        """
        Update a customer.

        :param data: the data to update.
        """
        return payplug.Customer.update(self, **data)

    def delete(self):
        """
        Delete the customer.
        """
        payplug.Customer.delete(self)

    def add_card(self, **data):
        """
        Add a card to the customer.

        :param data: The card data
        :return: The new card object
        :rtype Card
        """
        return payplug.Card.create(self, **data)

    def list_cards(self, *args, **kwargs):
        """
        List the cards of the customer.

        :param page: the page number
        :type page: int|None
        :param per_page: number of customers per page. It's a good practice to increase this number if you know that you
        will need a lot of payments.
        :type per_page: int|None
        :return: The cards of the customer
        :rtype APIResourceCollection
        """
        return payplug.Card.list(self, *args, **kwargs)


class Card(APIResource, ReconstituableAPIResource):
    """
    A Card Resource.
    """
    object_type = 'card'

    def delete(self):
        """
        Delete the card.
        """
        payplug.Card.delete(self.customer_id, self)


class APIResourceCollection(APIResource):
    """
    A class that contains multiple API resources
    """
    def __init__(self, expected_api_resource, **resource_attributes):
        """
        :param expected_api_resource: Type of collection object expected
        :type expected_api_resource: type(something that extends APIResource)
        :param resource_attributes: API resource parameters
        """
        object.__setattr__(self, '_expected_api_resource', expected_api_resource)

        super(APIResourceCollection, self).__init__(**resource_attributes)
        object.__setattr__(self, '_iterator', iter(self.data))

    def _initialize(self, **resource_attributes):
        """
        Initialize the collection.

        :param resource_attributes: API resource parameters
        """
        super(APIResourceCollection, self)._initialize(**resource_attributes)

        dict_list = self.data
        self.data = []
        for resource in dict_list:
            self.data.append(self._expected_api_resource(**resource))

    def __iter__(self):
        return self

    def next(self):
        return next(self._iterator)
    __next__ = next  # Python 3 compatibility

    def __getitem__(self, item):
        return self.data[item]


class AccountingReport(APIResource, VerifiableAPIResource, ReconstituableAPIResource):
    """
    An accounting report.
    """
    object_type = 'accounting_report'

    def get_consistent_resource(self):
        """
        :return an accounting report that you can trust.
        :rtype AccountingReport
        """
        http_client = HttpClient()
        response, _ = http_client.get(
            routes.url(routes.ACCOUNTING_REPORT_RESOURCE, resource_id=self.id)
        )
        return AccountingReport(**response)
