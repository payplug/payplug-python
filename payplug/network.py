# -*- coding: utf-8 -*-
import sys
import abc
import json
from six import with_metaclass
from payplug import config, exceptions
from payplug.__version__ import __version__


class HttpRequest(with_metaclass(abc.ABCMeta)):
    """
    Generic interface to abstract an HTTP Request.
    """
    def _raise_unrecoverable_error_payplug(self, exception):
        """
        Raises an exceptions.ClientError with a message telling that the error probably comes from PayPlug.
        :param exception: Exception that caused the ClientError.
        :type exception: Exception
        :raise exceptions.ClientError
        """
        message = ('There was an unrecoverable error during the HTTP request. It seems to come from our servers. '
                   'If you are behind a proxy, ensure that it is configured correctly. If the issue persists, do not '
                   'hesitate to contact us with the following information: `' + repr(exception) + '`.')
        raise exceptions.ClientError(message, client_exception=exception)

    def _raise_unrecoverable_error_client(self, exception):
        """
        Raises an exceptions.ClientError with a message telling that the error probably comes from the client
        configuration.
        :param exception: Exception that caused the ClientError
        :type exception: Exception
        :raise exceptions.ClientError
        """
        message = ('There was an unrecoverable error during the HTTP request which is probably related to your '
                   'configuration. Please verify `' + self.DEPENDENCY + '` library configuration and update it. If the '
                   'issue persists, do not hesitate to contact us with the following information: `' + repr(exception) +
                   '`.')
        raise exceptions.ClientError(message, client_exception=exception)

    @abc.abstractmethod
    def do_request(self, http_verb, url, headers, data=None):
        """
        Perform an HTTP request.

        :param http_verb: HTTP verb of the request ('GET', 'POST', 'PUT', …)
        :type http_verb: string
        :param url: URL of the request
        :type url: string
        :param headers: HTTP headers to pass to the request
        :type headers: dict
        :param data: additional data to pass in the request
        :type data: dict

        :return: request response, request HTTP status, request headers
        :rtype: tuple

        :raises
            exceptions.ClientError: When there was an unknown error with the HTTP client used for this request.
        """
        pass

    @staticmethod
    def get_useragent_string():
        """
        :return a string containing 'python-', the request library name, a slash and the library version.
        :example:
            - If version is available
            python-requests/2.0.0
            # If the version is not available:
            python-requests
        """
        raise NotImplementedError('get_useragent_string method must be implemented')


class RequestsRequest(HttpRequest):
    """
    HTTPRequest implementation that relies on requests library.
    """
    DEPENDENCY = 'requests'

    def do_request(self, http_verb, url, headers, data=None):
        """
        :see :func:`~HttpRequest.do_request`
        """
        if data:
            data = json.dumps(data)
        try:
            response = requests.request(http_verb, url, headers=headers, data=data, verify=config.CACERT_PATH)
        except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as exception:
            self._raise_unrecoverable_error_payplug(exception)
        except requests.exceptions.RequestException as exception:
            self._raise_unrecoverable_error_client(exception)

        return response.content, response.status_code, response.headers

    @staticmethod
    def get_useragent_string():
        return 'python-' + RequestsRequest.DEPENDENCY + '/' + requests.__version__


class UrllibRequest(HttpRequest):
    """
    HTTPRequest implementation that relies on urllib. Although it could help people who don't want to install requests
    dependency, using this implementation is not recommended.
    """
    DEPENDENCY = 'six'

    def do_request(self, http_verb, url, headers, data=None):
        """
        :see :func:`~HttpRequest.do_request`
        """
        if data:
            data = json.dumps(data)
        request = urllib.request.Request(url, data, headers)
        request.get_method = lambda: http_verb

        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as response_:
            response = response_
        except urllib.error.URLError as exception:
            if isinstance(exception.reason, socket.timeout):  # Python 2.6
                self._raise_unrecoverable_error_payplug(exception)
            else:
                self._raise_unrecoverable_error_client(exception)
        except socket.timeout as exception:  # Python 2.7+
            self._raise_unrecoverable_error_payplug(exception)
        except http_client.HTTPException as exception:
            self._raise_unrecoverable_error_client(exception)

        return response.read(), response.code, dict(response.info())

    @staticmethod
    def get_useragent_string():
        return 'python-' + UrllibRequest.DEPENDENCY + '-urllib/' + six.__version__


available_clients = []

try:
    import requests
except ImportError:
    pass
else:
    available_clients.append(RequestsRequest)

try:
    import six
    from six.moves import urllib, http_client
    import socket
except ImportError:
    pass
else:
    available_clients.append(UrllibRequest)


class HttpClient(object):
    """
    HTTP Client that relies on HttpRequest to perform requests.
    """
    def __init__(self, token=None, request_handler=None, api_version=None):
        """
        :param token: the secret key that will be used to authenticate API requests
        :type token: string
        :param request_handler: the HttpRequest that will handle the requests. Default is RequestsRequest if `requests`
            is installed. Else, it will try to fallback to UrllibRequest. Provided class type must inherit HttpRequest.
        :type request_handler: types.ClassType
        """
        if not request_handler and not available_clients:
            raise RuntimeError('No suitable library to perform HTTP requests found.')

        if not token and not config.secret_key:
            raise exceptions.SecretKeyNotSet('You must set your secret key using payplug.set_secret_key() function.')

        self._secret_key = token or config.secret_key
        self._api_version = api_version or config.api_version
        self._request_handler = request_handler or available_clients[0]

    def post(self, url, data=None):
        """
        Send an authenticated POST request to the API.

        :param url: url to the remote resource
        :type url: string
        :param data: request data
        :type data: dict|None

        :return: http response, http status
        :rtype tuple(string, int)


        :raises
            exception.HttpError when http request returned bad HTTP status (≠ 2xx).
            exception.ClientError on unexpected error
        """
        return self._request('POST', url, data)

    def patch(self, url, data=None):
        """
        Send an authenticated PATCH request to the API.

        :param url: url to the remote resource
        :type url: string
        :param data: request data
        :type data: dict|None

        :return: http response, http status
        :rtype tuple(string, int)


        :raises
            exception.HttpError when http request returned bad HTTP status (≠ 2xx).
            exception.ClientError on unexpected error
        """
        return self._request('PATCH', url, data)

    def delete(self, url, data=None):
        """
        Send an authenticated DELETE request to the API.

        :param url: url to the remote resource
        :type url: string
        :param data: request data
        :type data: dict|None

        :return: http response, http status
        :rtype tuple(string, int)


        :raises
            exception.HttpError when http request returned bad HTTP status (≠ 2xx).
            exception.ClientError on unexpected error
        """
        return self._request('DELETE', url, data)

    def get(self, url):
        """
        Send an authenticated GET request to the API.

        :param url: url to the remote resource
        :type url: string

        :return: http response, http status
        :rtype tuple(string, int)


        :raises
            exception.HttpError when http request returned bad HTTP status (≠ 2xx).
            exception.ClientError on unexpected error
        """
        return self._request('GET', url)

    def _request(self, http_verb, url, data=None, authenticated=True):
        """
        Perform an HTTP request.

        See https://docs.python.org/3/library/json.html#json-to-py-table for the http response object.

        :param http_verb: the HTTP verb (GET, POST, PUT, …)
        :type http_verb: string
        :param url: the path to the resource queried
        :type url: string
        :param data: the request content
        :type data: dict
        :param authenticated: the request should be authenticated
        :type authenticated: bool

        :return: http response, http status
        :rtype tuple(object, int)
        """
        user_agent = ('PayPlug-Python/{lib_version} (Python/{python_version}; '
                      '{request_library})'
                      .format(lib_version=__version__,
                              python_version=_get_python_version_string(),
                              request_library=self._request_handler.get_useragent_string()))
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': user_agent,
        }
        if authenticated:
            headers['Authorization'] = 'Bearer ' + self._secret_key

        if self._api_version:
            headers['PayPlug-Version'] = self._api_version

        requestor = self._request_handler()
        response, status, _ = requestor.do_request(http_verb, url, headers, data)

        # Since Python 3.2+, response body is a bytes-like object. We have to decode it to a string.
        if isinstance(response, six.binary_type):
            response = response.decode('utf-8')

        if not 200 <= status < 300:
            raise exceptions.HttpError.map_http_status_to_exception(status)(http_response=response,
                                                                            http_status=status)

        try:
            response_object = json.loads(response)
        except ValueError:
            raise exceptions.UnexpectedAPIResponseException(http_response=response, http_status=status)

        return response_object, status


def _get_python_version_string():
    """
    Returns a string representation of the Python version.

    :return: "2.7.8" if python version is 2.7.8.
    :rtype string
    """
    version_info = sys.version_info
    return '.'.join(map(str, [version_info[0], version_info[1], version_info[2]]))
