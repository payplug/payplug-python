# -*- coding: utf-8 -*-
from six import string_types
from payplug import config, exceptions, resources, routes
from payplug.network import HttpClient
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


def set_api_version(version):
    """
    Specify the PayPlug API version to use.

    :Example

    >>> import payplug
    >>> payplug.set_api_version("2019-08-06")

    :param version: the desired version, as an ISO-8601 date
    :type version: string
    """

    if not isinstance(version, string_types) and version is not None:
        raise exceptions.ConfigurationError('Expected string value for API version.')

    config.api_version = version


class Payment(object):
    """
    A DAO for resources.Payment which provides a way to query payment resources.
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
        response, __ = http_client.get(routes.url(routes.PAYMENT_RESOURCE, resource_id=payment_id))
        return resources.Payment(**response)

    @staticmethod
    def abort(payment):
        """
        Abort a payment from its id.

        :param payment: The payment id or payment object
        :type payment: string|Payment

        :return: The payment resource
        :rtype: resources.Payment
        """
        if isinstance(payment, resources.Payment):
            payment = payment.id

        http_client = HttpClient()
        response, __ = http_client.patch(routes.url(routes.PAYMENT_RESOURCE, resource_id=payment), {'abort': True})
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
        response, _ = http_client.post(routes.url(routes.PAYMENT_RESOURCE), data)
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
        response, _ = http_client.get(routes.url(routes.PAYMENT_RESOURCE, pagination=pagination))
        return resources.APIResourceCollection(resources.Payment, **response)


class Refund(object):
    """
    A DAO for resources.Refund which provides a way to query refund resources.
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
        response, _ = http_client.get(routes.url(routes.REFUND_RESOURCE, resource_id=refund_id, payment_id=payment))
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
        response, _ = http_client.post(routes.url(routes.REFUND_RESOURCE, payment_id=payment), data)
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
        response, _ = http_client.get(routes.url(routes.REFUND_RESOURCE, payment_id=payment))
        return resources.APIResourceCollection(resources.Refund, **response)


class Customer(object):
    """
    A DAO for resources.Customer which provides a way to query customer resources.
    """
    @staticmethod
    def retrieve(customer_id):
        """
        Retrieve a customer from its id.

        :param customer_id: The customer id
        :type customer_id: string

        :return: The customer resource
        :rtype: resources.Customer
        """
        http_client = HttpClient()
        response, __ = http_client.get(routes.url(routes.CUSTOMER_RESOURCE, resource_id=customer_id))
        return resources.Customer(**response)

    @staticmethod
    def delete(customer):
        """
        Delete a customer from its id.

        :param customer: The customer id or object
        :type customer: string|Customer
        """
        if isinstance(customer, resources.Customer):
            customer = customer.id

        http_client = HttpClient()
        http_client.delete(routes.url(routes.CUSTOMER_RESOURCE, resource_id=customer))

    @staticmethod
    def update(customer, **data):
        """
        Update a customer from its id.

        :param customer: The customer id or object
        :type customer: string|Customer
        :param data: The data you want to update

        :return: The customer resource
        :rtype resources.Customer
        """
        if isinstance(customer, resources.Customer):
            customer = customer.id

        http_client = HttpClient()
        response, _ = http_client.patch(routes.url(routes.CUSTOMER_RESOURCE, resource_id=customer), data)
        return resources.Customer(**response)

    @staticmethod
    def create(**data):
        """
        Create a customer.

        :param data: data required to create the customer

        :return: The customer resource
        :rtype resources.Customer
        """
        http_client = HttpClient()
        response, _ = http_client.post(routes.url(routes.CUSTOMER_RESOURCE), data)
        return resources.Customer(**response)

    @staticmethod
    def list(per_page=None, page=None):
        """
        List of customers. You have to handle pagination manually for the moment.

        :param page: the page number
        :type page: int|None
        :param per_page: number of customers per page. It's a good practice to increase this number if you know that you
        will need a lot of payments.
        :type per_page: int|None

        :return A collection of customers
        :rtype resources.APIResourceCollection
        """
        # Comprehension dict are not supported in Python 2.6-. You can use this commented line instead of the current
        # line when you drop support for Python 2.6.
        # pagination = {key: value for (key, value) in [('page', page), ('per_page', per_page)] if value}
        pagination = dict((key, value) for (key, value) in [('page', page), ('per_page', per_page)] if value)

        http_client = HttpClient()
        response, _ = http_client.get(routes.url(routes.CUSTOMER_RESOURCE, pagination=pagination))
        return resources.APIResourceCollection(resources.Customer, **response)


class Card(object):
    """
    A DAO for resources.Card which provides a way to query customer resources.
    """
    @staticmethod
    def retrieve(customer, card_id):
        """
        Retrieve a card from its id.

        :param customer: The customer id or object
        :type customer: string|Customer
        :param card_id: The card id
        :type card_id: string

        :return: The customer resource
        :rtype: resources.Card
        """
        if isinstance(customer, resources.Customer):
            customer = customer.id

        http_client = HttpClient()
        response, __ = http_client.get(routes.url(routes.CARD_RESOURCE, resource_id=card_id, customer_id=customer))
        return resources.Card(**response)

    @staticmethod
    def delete(customer, card):
        """
        Delete a card from its id.

        :param customer: The customer id or object
        :type customer: string|Customer
        :param card: The card id or object
        :type card: string|Card
        """
        if isinstance(customer, resources.Customer):
            customer = customer.id
        if isinstance(card, resources.Card):
            card = card.id

        http_client = HttpClient()
        http_client.delete(routes.url(routes.CARD_RESOURCE, resource_id=card, customer_id=customer))

    @staticmethod
    def create(customer, **data):
        """
        Create a card instance.

        :param customer: the customer id or object
        :type customer: string|Customer
        :param data: data required to create the card

        :return: The card resource
        :rtype resources.Card
        """
        if isinstance(customer, resources.Customer):
            customer = customer.id

        http_client = HttpClient()
        response, _ = http_client.post(routes.url(routes.CARD_RESOURCE, customer_id=customer), data)
        return resources.Card(**response)

    @staticmethod
    def list(customer, per_page=None, page=None):
        """
        List of cards. You have to handle pagination manually for the moment.

        :param customer: the customer id or object
        :type customer: string|Customer
        :param page: the page number
        :type page: int|None
        :param per_page: number of customers per page. It's a good practice to increase this number if you know that you
        will need a lot of payments.
        :type per_page: int|None

        :return A collection of cards
        :rtype resources.APIResourceCollection
        """
        if isinstance(customer, resources.Customer):
            customer = customer.id

        # Comprehension dict are not supported in Python 2.6-. You can use this commented line instead of the current
        # line when you drop support for Python 2.6.
        # pagination = {key: value for (key, value) in [('page', page), ('per_page', per_page)] if value}
        pagination = dict((key, value) for (key, value) in [('page', page), ('per_page', per_page)] if value)

        http_client = HttpClient()
        response, _ = http_client.get(routes.url(routes.CARD_RESOURCE, customer_id=customer, pagination=pagination))
        return resources.APIResourceCollection(resources.Card, **response)


class AccountingReport:
    """
    A DAO for resources.AccountingReport which provides a way to query accounting reports.
    """
    @staticmethod
    def retrieve(report_id):
        """
        Retrieve an accounting report from its id.

        :param report_id: The report id
        :type report_id: string

        :return: The accounting report resource
        :rtype: resources.AccountingReport
        """
        http_client = HttpClient()
        response, __ = http_client.get(routes.url(routes.ACCOUNTING_REPORT_RESOURCE, resource_id=report_id))
        return resources.AccountingReport(**response)

    @staticmethod
    def create(**data):
        """
        Create an accounting report.

        :param data: data required to create the report

        :return: The accounting report resource
        :rtype resources.AccountingReport
        """
        http_client = HttpClient()
        response, _ = http_client.post(routes.url(routes.ACCOUNTING_REPORT_RESOURCE), data)
        return resources.AccountingReport(**response)
