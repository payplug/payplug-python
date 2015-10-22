# -*- coding: utf-8 -*-
import pytest
from mock import patch, MagicMock

from six.moves import urllib
import sys
from payplug import network
from payplug.test import TestBase

@pytest.mark.xfail(sys.version_info < (2, 7, 9), reason="Can't set ca_file easily with urllib.")
class TestUrllibRequest(TestBase):
    @pytest.fixture(scope='class')
    def urllib_urlopen_200_fixture(self):
        response_obj_mock = MagicMock(code=200)
        response_obj_mock.read.return_value = 'OK'
        response_obj_mock.info.return_value = {'header': 'header_value'}
        response_mock = MagicMock(return_value=response_obj_mock)
        return response_mock

    @pytest.fixture(scope='class')
    def urllib_urlopen_500_fixture(self):
        http_error_fp_read = MagicMock()
        http_error_fp_read.read.return_value = 'KO'
        http_error = urllib.error.HTTPError('error_url', 500, 'msg', None, http_error_fp_read)
        http_error.info = MagicMock(return_value={'header': 'header_value'})

        return MagicMock(side_effect=http_error)

    @patch('payplug.network.json.dumps', return_value='{"some":"data"}')
    @patch('payplug.network.config')
    @patch('payplug.network.urllib.request.Request')
    def test_do_request_ok(self, urllib_request_mock, config_mock, json_dumps_mock, urllib_urlopen_200_fixture):
        config_mock.configure_mock(CACERT_PATH='cacert_path')

        urllib_request_object_mock = MagicMock()
        urllib_request_mock.return_value = urllib_request_object_mock

        request = network.UrllibRequest()

        with patch('payplug.network.urllib.request.urlopen', urllib_urlopen_200_fixture):
            response = request.do_request('GET', 'http://example.com', {}, {'some': 'data'})

        urllib_request_mock.assert_called_once_with('http://example.com', '{"some":"data"}', {})
        urllib_urlopen_200_fixture.assert_called_once_with(urllib_request_object_mock)

        assert ('OK', 200, {'header': 'header_value'}) == response

        assert json_dumps_mock.called_once_with({'some': 'data'})

    @patch('payplug.network.config')
    @patch('payplug.network.urllib.request.Request')
    def test_do_request_http_error(self, urllib_request_mock, config_mock, urllib_urlopen_500_fixture):
        config_mock.configure_mock(CACERT_PATH='cacert_path')

        urllib_request_object_mock = MagicMock()
        urllib_request_mock.return_value = urllib_request_object_mock

        request = network.UrllibRequest()

        with patch('payplug.network.urllib.request.urlopen', urllib_urlopen_500_fixture):
            response = request.do_request('GET', 'http://example.com', {}, {})

        urllib_request_mock.assert_called_once_with('http://example.com', {}, {})

        assert ('KO', 500, {'header': 'header_value'}) == response

    def test_get_user_agent_string(self):
        user_agent_string = network.UrllibRequest.get_useragent_string()
        assert user_agent_string.startswith('python-six-urllib/')
