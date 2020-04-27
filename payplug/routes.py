# -*- coding: utf-8 -*-
from six.moves.urllib.parse import urlencode

# Resources URL
PAYMENT_RESOURCE = '/payments'
REFUND_RESOURCE = PAYMENT_RESOURCE + '/{payment_id}/refunds'
CUSTOMER_RESOURCE = '/customers'
CARD_RESOURCE = CUSTOMER_RESOURCE + '/{customer_id}/cards'
ACCOUNTING_REPORT_RESOURCE = '/accounting_reports'

# API base url
API_BASE_URL = 'https://api.payplug.com'
API_VERSION = 1


def url(route, resource_id=None, pagination=None, **parameters):
    """
    Generates an absolute URL to an API resource.

    :param route: One of the routes available (see the header of this file)
    :type route: string
    :param resource_id: The resource ID you want. If None, it will point to the endpoint.
    :type resource_id: string|None
    :param pagination: parameters for pagination
    :type pagination: dict|None
    :param parameters: additional parameters required by the route

    :return the absolute route to the API
    :rtype string
    """
    route = route.format(**parameters)

    resource_id_url = '/' + str(resource_id) if resource_id else ''

    query_parameters = ''
    if pagination:
        query_parameters += urlencode(pagination)
    if query_parameters:
        query_parameters = '?' + query_parameters

    return _base_url() + route + resource_id_url + query_parameters


def _base_url():
    """
    :return: The base URL to the API
    """
    return API_BASE_URL + '/v' + str(API_VERSION)
