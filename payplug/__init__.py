# -*- coding: utf-8 -*-
from six import string_types
from payplug import config, exceptions, network, notifications, resources, routes
from payplug.network import HttpClient, UrllibRequest
from payplug.__version__ import __version__


__author__ = 'PayPlug Team <support@payplug.com>'
__version__ = __version__


def set_secret_key(token):
    """
    Initializes a Authentication and sets it as the new default global authentication.
    It also performs some checks before saving the authentication.

    :Example

    >>> # Expected format for secret key:
    >>> import payplug
    >>> payplug.set_secret_key('sk_test_somerandomcharacters')

    :param token: your secret token (live or sandbox)
    :type token: string
    """
    if not isinstance(token, string_types):
        raise exceptions.ConfigurationError('Expected string value for token.')

    config.secret_key = token


class Payment(object):
    """
    A DAO for resources.Payment which provides an cromulent way to query payment resources.
    """
    @staticmethod
    def retrieve(payment_id):
        """
        Retrieve a payment from its id.

        :param payment_id: The payment id
        :type payment_id: string

        :return: The payment resource
        :rtype: resources.Payment
        """
        http_client = HttpClient()
        response, __ = http_client.get(routes.url(routes.RETRIEVE_PAYMENT, payment_id=payment_id))
        return resources.Payment(**response)

    @staticmethod
    def create(**data):
        """
        Create a Payment request.

        :param data: data required to create the payment

        :return: The payment resource
        :rtype resources.Payment
        """
        http_client = HttpClient()
        response, _ = http_client.post(routes.url(routes.CREATE_PAYMENT), data)
        return resources.Payment(**response)

    @staticmethod
    def list(per_page=None, page=None):
        """
        List of payments. You have to handle pagination manually

        :param page: the page number
        :type page: int|None
        :param per_page: number of payment per page. It's a good practice to increase this number if you know that you
        will need a lot of payments.
        :type per_page: int|None

        :return A collection of payment
        :rtype resources.APIResourceCollection
        """
        # Comprehension dict are not supported in Python 2.6-. You can use this commented line instead of the current
        # line when you drop support for Python 2.6.
        # pagination = {key: value for (key, value) in [('page', page), ('per_page', per_page)] if value}
        pagination = dict((key, value) for (key, value) in [('page', page), ('per_page', per_page)] if value)

        http_client = HttpClient()
        response, _ = http_client.get(routes.url(routes.LIST_PAYMENTS, pagination))
        return resources.APIResourceCollection(resources.Payment, **response)


class Refund(object):
    """
    A DAO for resources.Refund which provides an cromulent way to query refund resources.
    """
    @staticmethod
    def retrieve(payment, refund_id):
        """
        Retrieve a refund from a payment and the refund id.

        :param payment: The payment id or the payment object
        :type payment: resources.Payment|string
        :param refund_id: The refund id
        :type refund_id: string

        :return: The refund resource
        :rtype: resources.Refund
        """
        if isinstance(payment, resources.Payment):
            payment = payment.id

        http_client = HttpClient()
        response, _ = http_client.get(routes.url(routes.RETRIEVE_REFUND, payment_id=payment, refund_id=refund_id))
        return resources.Refund(**response)

    @staticmethod
    def create(payment, **data):
        """
        Create a refund on a payment.

        :param payment: Either the payment object or the payment id you want to refund.
        :type payment: resources.Payment|string
        :param data: data required to create the refund

        :return: The refund resource
        :rtype resources.Refund
        """
        if isinstance(payment, resources.Payment):
            payment = payment.id

        http_client = HttpClient()
        response, _ = http_client.post(routes.url(routes.CREATE_REFUND, payment_id=payment), data)
        return resources.Refund(**response)

    @staticmethod
    def list(payment):
        """
        List all the refunds for a payment.

        :param payment: The payment object or the payment id
        :type payment: resources.Payment|string

        :return: A collection of refunds
        :rtype resources.APIResourceCollection
        """
        if isinstance(payment, resources.Payment):
            payment = payment.id

        http_client = HttpClient()
        response, _ = http_client.get(routes.url(routes.LIST_REFUNDS, payment_id=payment))
        return resources.APIResourceCollection(resources.Refund, **response)
