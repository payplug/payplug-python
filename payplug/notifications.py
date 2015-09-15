# -*- coding: utf-8 -*-
import json
import six
from payplug import exceptions
from payplug.resources import APIResource


def treat(request_body):
    """
    Treat a notification and guarantee its authenticity.

    :param request_body: The request body in plain text.
    :type request_body: string

    :return: A safe APIResource
    :rtype: APIResource
    """
    # Python 3+ support
    if isinstance(request_body, six.binary_type):
        request_body = request_body.decode('utf-8')

    try:
        data = json.loads(request_body)
    except ValueError:
        raise exceptions.UnknownAPIResource('Request body is malformed JSON.')

    unsafe_api_resource = APIResource.factory(data)

    try:
        consistent_api_resource = unsafe_api_resource.get_consistent_resource()
    except AttributeError:
        raise exceptions.UnknownAPIResource('The API resource provided is invalid.')

    return consistent_api_resource
