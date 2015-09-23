# -*- coding: utf-8 -*-
from mock import patch, MagicMock
import pytest
from payplug import network, HttpClient, exceptions
from payplug.test import TestBase


class TestHttpClient(TestBase):
    @patch('payplug.network.available_clients', [])
    def test_missing_dependencies(self):
        with pytest.raises(RuntimeError) as excinfo:
            HttpClient()
        assert str(excinfo.value) == 'No suitable library to perform HTTP requests found.'

    @patch('payplug.network.available_clients', [network.RequestsRequest])
    @patch('payplug.config.secret_key', 'a_secret_key')
    def test_default_secret_key(self):
        http_client = HttpClient()
        assert http_client._secret_key == 'a_secret_key'

    @patch('payplug.network.available_clients', [network.RequestsRequest])
    @patch('payplug.config.secret_key', 'a_secret_key')
    def test_secret_key(self):
        http_client = HttpClient(token='another_secret_key')
        assert http_client._secret_key == 'another_secret_key'

    @patch('payplug.network.available_clients', [network.RequestsRequest])
    @patch('payplug.config.secret_key', None)
    def test_default_no_secret_key(self):
        with pytest.raises(exceptions.SecretKeyNotSet):
            HttpClient()

    @patch('payplug.network.available_clients', [network.RequestsRequest, network.UrllibRequest])
    @patch('payplug.config.secret_key', 'a_secret_key')
    def test_default_request_handler(self):
        http_client = HttpClient()
        assert http_client._request_handler == network.RequestsRequest

    @patch('payplug.network.available_clients', [network.RequestsRequest, network.UrllibRequest])
    @patch('payplug.config.secret_key', 'a_secret_key')
    def test_request_handler(self):
        http_client = HttpClient(request_handler=network.UrllibRequest)
        assert http_client._request_handler == network.UrllibRequest

    @patch('payplug.network.HttpClient._request')
    def test_post(self, _request_mock):
        http_client = HttpClient('a_secret_key', MagicMock())
        http_client.post('this_is_an_url', {'data': 'tada'})
        _request_mock.assert_called_once_with('POST', 'this_is_an_url', {'data': 'tada'})

    @patch('payplug.network.HttpClient._request')
    def test_patch(self, _request_mock):
        http_client = HttpClient('a_secret_key', MagicMock())
        http_client.patch('this_is_an_url', {'data': 'tada'})
        _request_mock.assert_called_once_with('PATCH', 'this_is_an_url', {'data': 'tada'})

    @patch('payplug.network.HttpClient._request')
    def test_get(self, _request_mock):
        http_client = HttpClient('a_secret_key', MagicMock())
        http_client.get('this_is_an_url')
        _request_mock.assert_called_once_with('GET', 'this_is_an_url')

    def test_request_ok(self):
        requestor = MagicMock()
        requestor.do_request.return_value = '"a valid json response"', 201, {}
        request_handler = MagicMock(return_value=requestor)

        http_client = HttpClient('a_secret_key', request_handler)
        response, status = http_client._request('POST', 'this_is_an_url', {'some': 'data'})

        assert requestor.do_request.call_count == 1
        do_request_args, _ = requestor.do_request.call_args
        assert do_request_args[0] == 'POST'
        assert do_request_args[1] == 'this_is_an_url'
        assert do_request_args[2]['Authorization'] == 'Bearer a_secret_key'
        assert do_request_args[3] == {'some': 'data'}

        assert response == 'a valid json response'
        assert status == 201

    def test_request_500(self):
        requestor = MagicMock()
        requestor.do_request.return_value = '"a valid json response"', 500, {}
        request_handler = MagicMock(return_value=requestor)

        http_client = HttpClient('a_secret_key', request_handler)

        with pytest.raises(exceptions.PayPlugServerError) as excinfo:
            http_client._request('POST', 'this_is_an_url', {'some': 'data'})

        server_error = excinfo.value
        assert '"a valid json response"' in str(server_error)

    def test_request_unexpected_api_response(self):
        requestor = MagicMock()
        requestor.do_request.return_value = 'an invalid json response"', 200, {}
        request_handler = MagicMock(return_value=requestor)

        http_client = HttpClient('a_secret_key', request_handler)

        with pytest.raises(exceptions.UnexpectedAPIResponseException):
            http_client._request('GET', 'this_is_an_url', {'some': 'data'})
