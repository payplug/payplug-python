# -*- coding: utf-8 -*-
from payplug import exceptions
from payplug.test import TestBase


class TestHttpError(TestBase):
    def test_get_response_code(self):
        http_error = exceptions.HttpError(http_status=500, http_response=None)
        assert http_error.http_response_code == 500

    def test_get_error_object_valid_json(self):
        http_error = exceptions.HttpError(http_status=500, http_response='["valid", "json", "response"]')
        assert http_error.error_object == ['valid', 'json', 'response']

    def test_get_error_object_invalid_json(self):
        http_error = exceptions.HttpError(http_status=500, http_response='["invalid", "json", "response"')
        assert http_error.error_object is None

    def test_map_http_code_to_exception(self):
        assert exceptions.HttpError.map_http_status_to_exception(400) == exceptions.BadRequest
        assert exceptions.HttpError.map_http_status_to_exception(401) == exceptions.Unauthorized
        assert exceptions.HttpError.map_http_status_to_exception(403) == exceptions.Forbidden
        assert exceptions.HttpError.map_http_status_to_exception(404) == exceptions.NotFound
        assert exceptions.HttpError.map_http_status_to_exception(405) == exceptions.NotAllowed
        assert exceptions.HttpError.map_http_status_to_exception(500) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(501) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(502) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(503) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(504) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(505) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(506) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(507) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(508) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(509) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(510) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(511) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(520) == exceptions.PayPlugServerError
        assert exceptions.HttpError.map_http_status_to_exception(302) == exceptions.HttpError

    def test_messages(self):
        assert 'Unhandled HTTP error' in str(exceptions.HttpError())
        assert 'Bad request' in str(exceptions.BadRequest())
        assert 'Unauthorized. Please check your secret key' in str(exceptions.Unauthorized())
        assert 'Forbidden error. You are not allowed to access this resource' in str(exceptions.Forbidden())
        assert 'The resource you requested could not be found' in str(exceptions.NotFound())
        assert 'The requested method is not supported by this resource' in str(exceptions.NotAllowed())
        assert 'Unexpected server error during the request' in str(exceptions.PayPlugServerError())
        assert 'API response is not valid JSON' in str(exceptions.UnexpectedAPIResponseException())

    def test_response_included_in_message(self):
        assert ('The server gave the following response: `"a response"`.' in
                str(exceptions.HttpError(http_response='"a response"')))


class TestClientError:
    def test_get_client_exception(self):
        client_exception = ValueError('foo bar')
        client_error = exceptions.ClientError(client_exception=client_exception)
        assert client_error.get_client_exception == client_exception
