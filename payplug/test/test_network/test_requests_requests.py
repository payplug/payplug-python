# -*- coding: utf-8 -*-
import pytest
from mock import patch, MagicMock
import requests

from payplug import exceptions, network
from payplug.test import TestBase


class TestRequestsRequest(TestBase):
    @pytest.fixture(scope='class')
    def requests_request_200_fixture(self):
        return MagicMock(return_value=MagicMock(content='OK', status_code=200, headers={}))

    @pytest.fixture(scope='class')
    def requests_request_timeout_fixture(self):
        return MagicMock(side_effect=requests.exceptions.Timeout())

    @pytest.fixture(scope='class')
    def requests_request_too_many_redirects_fixture(self):
        return MagicMock(side_effect=requests.exceptions.TooManyRedirects())

    @pytest.fixture(scope='class')
    def requests_request_request_exception_fixture(self):
        return MagicMock(side_effect=requests.exceptions.RequestException())

    @patch('payplug.network.config')
    def test_do_request_ok(self, config_mock, requests_request_200_fixture):
        config_mock.configure_mock(CACERT_PATH='cacert_path')
        request = network.RequestsRequest()

        with patch('payplug.network.requests.request', requests_request_200_fixture):
            response = request.do_request('GET', 'http://example.com', {}, {})

        requests_request_200_fixture.assert_called_once_with(
            'GET', 'http://example.com', headers={}, data={}, verify='cacert_path'
        )

        assert ('OK', 200, {}) == response

    def test_do_request_timeout(self, requests_request_timeout_fixture):
        request = network.RequestsRequest()

        with pytest.raises(exceptions.ClientError) as excinfo:
            with patch('payplug.network.requests.request', requests_request_timeout_fixture):
                request.do_request('GET', 'http://example.com', {}, {})
        assert isinstance(excinfo.value.get_client_exception, requests.exceptions.Timeout)

    def test_do_request_too_many_redirects(self, requests_request_too_many_redirects_fixture):
        request = network.RequestsRequest()

        with pytest.raises(exceptions.ClientError) as excinfo:
            with patch('payplug.network.requests.request', requests_request_too_many_redirects_fixture):
                request.do_request('GET', 'http://example.com', {}, {})
        assert isinstance(excinfo.value.get_client_exception, requests.exceptions.TooManyRedirects)
        assert 'It seems to come from our servers.' in str(excinfo.value)

    def test_do_request_request_exception(self, requests_request_request_exception_fixture):
        request = network.RequestsRequest()

        with pytest.raises(exceptions.ClientError) as excinfo:
            with patch('payplug.network.requests.request', requests_request_request_exception_fixture):
                request.do_request('GET', 'http://example.com', {}, {})
        assert isinstance(excinfo.value.get_client_exception, requests.exceptions.RequestException)
        assert 'Please verify `requests` library configuration and update it.' in str(excinfo.value)

    def test_get_user_agent_string(self):
        user_agent_string = network.RequestsRequest.get_useragent_string()
        assert user_agent_string.startswith('python-requests/')
