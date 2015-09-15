# -*- coding: utf-8 -*-
from six.moves.urllib.parse import urlencode

# Payments routes
CREATE_PAYMENT = '/payments'
RETRIEVE_PAYMENT = '/payments/{payment_id}'
LIST_PAYMENTS = '/payments'

# Refunds routes
CREATE_REFUND = '/payments/{payment_id}/refunds'
RETRIEVE_REFUND = '/payments/{payment_id}/refunds/{refund_id}'
LIST_REFUNDS = '/payments/{payment_id}/refunds'

# API base url
API_BASE_URL = 'https://api.payplug.com'
API_VERSION = 1


def url(route, pagination=None, **parameters):
    """
    Generates an absolute URL to an API resource.

    :param route: One of the routes available (see the header of this file)
    :type route: string
    :param pagination: parameters for pagination
    :type pagination: dict|None
    :param parameters: additional parameters required by the route

    :return the absolute route to the API
    :rtype string
    """
    route = route.format(**parameters)

    query_parameters = ''
    if pagination:
        query_parameters += urlencode(pagination)
    if query_parameters:
        query_parameters = '?' + query_parameters

    return _base_url() + route + query_parameters


def _base_url():
    """
    :return: The base URL to the API
    """
    return API_BASE_URL + '/v' + str(API_VERSION)
