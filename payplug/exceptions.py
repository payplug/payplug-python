# -*- coding: utf-8 -*-
import json


class PayplugError(Exception):
    """
    Generic Payplug exception.
    """
    pass


class ConfigurationError(PayplugError):
    """
    Configuration failure.
    """
    pass


class SecretKeyNotSet(PayplugError):
    """
    Trying to process a request despite the fact that the secret key was not set.
    If this is raised, you should define a configuration first:
    >>> import payplug
    >>> payplug.set_secret_key('your_secret_token')
    """
    pass


class ClientError(PayplugError):
    """
    Raised when there was an unrecoverable error during the request.
    This is not an unexpected HTTP response code. For HTTP client error or server errors, see :func:`~HttpError`
    """
    def __init__(self, message=None, client_exception=None):
        """
        :param client_exception: Exception raised by the client
        :type client_exception: Exception
        """
        super(ClientError, self).__init__(message)
        self._client_exception = client_exception

    @property
    def client_exception(self):
        """
        :return The client exception attached to this exception
        """
        return self._client_exception


class UnknownAPIResource(PayplugError):
    """
    Raised when it's impossible to reconstruct the APIResource from its data.
    """
    pass


class HttpError(PayplugError):
    """
    Raised when the HTTP Response code of a Request is invalid.
    """
    MESSAGE = 'Unhandled HTTP error.'

    def __init__(self, http_response=None, http_status=None, message=None):
        """
        :param http_status: The HTTP response code.
        :type http_status: int
        """
        self._http_response_code = http_status
        self._http_response = http_response

        if not message:
            message = self.MESSAGE
        super(HttpError, self).__init__(message)

    def __str__(self):
        ret = super(HttpError, self).__str__()
        if self._http_response:
            ret += ' The server gave the following response: `' + self._http_response + '`.'
        return ret

    @property
    def http_response_code(self):
        """
        :return The HTTP code returned in response.
        :rtype int
        """
        return self._http_response_code

    @property
    def error_object(self):
        """
        Try to parse the HTTP response as JSON and return the decoded object.

        :return The parsed JSON data or None if it's not valid JSON
        """
        try:
            return json.loads(self._http_response)
        except ValueError:  # includes JSONDecodeError
            return None

    @staticmethod
    def map_http_status_to_exception(http_code):
        """
        Bind a HTTP status to an HttpError.

        :param http_code: The HTTP code
        :type http_code: int

        :return The HttpError that fits to the http_code or HttpError.
        :rtype Any subclass of HttpError or HttpError
        """
        http_exceptions = HttpError.__subclasses__()
        for http_exception in http_exceptions:
            http_statuses = http_exception.HTTP_STATUSES
            if isinstance(http_statuses, int):
                http_statuses = [http_exception.HTTP_STATUSES]

            try:
                if http_code in http_statuses:
                    return http_exception
            except TypeError:  # Pass if statuses is not iterable (≈ None)
                pass

        return HttpError


class BadRequest(HttpError):
    """
    HTTP Error 400
    """
    HTTP_STATUSES = 400
    MESSAGE = 'Bad request.'
    pass


class Unauthorized(HttpError):
    """
    HTTP Error 401
    """
    HTTP_STATUSES = 401
    MESSAGE = 'Unauthorized. Please check your secret key.'
    pass


class Forbidden(HttpError):
    """
    HTTP Error 403
    """
    HTTP_STATUSES = 403
    MESSAGE = 'Forbidden error. You are not allowed to access this resource.'
    pass


class NotFound(HttpError):
    """
    HTTP Error 404
    """
    HTTP_STATUSES = 404
    MESSAGE = 'The resource you requested could not be found.'
    pass


class NotAllowed(HttpError):
    """
    HTTP Error 405
    """
    HTTP_STATUSES = 405
    MESSAGE = 'The requested method is not supported by this resource.'
    pass


class PayPlugServerError(HttpError):
    """
    HTTP Error 500
    """
    HTTP_STATUSES = [i for i in range(500, 600)]
    MESSAGE = 'Unexpected server error during the request.'
    pass


class UnexpectedAPIResponseException(HttpError):
    """
    Raised when we expected the API to have a specific format, and we got something else.
    """
    HTTP_STATUSES = None
    MESSAGE = 'API response is not valid JSON.'
    pass
