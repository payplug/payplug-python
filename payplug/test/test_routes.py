# -*- coding: utf-8 -*-
from mock import patch
from payplug import routes
from payplug.test import TestBase


@patch('payplug.routes.API_BASE_URL', 'http://payplug.com')
@patch('payplug.routes.API_VERSION', 1)
class TestRoutes(TestBase):
    def test_base_url(self):
        assert routes._base_url() == 'http://payplug.com/v1'

    def test_url_without_format(self):
        assert routes.url('/test') == 'http://payplug.com/v1/test'

    def test_url_with_format(self):
        assert routes.url('/foo/{val}', val='bar') == 'http://payplug.com/v1/foo/bar'
        assert routes.url('/payments/{payment_id}', payment_id='112358') == 'http://payplug.com/v1/payments/112358'

    def test_url_with_format_and_paginator(self):
        url = routes.url('/foo/{val}', pagination={'page': 2, 'per_page': 20}, val='bar')
        assert url.startswith('http://payplug.com/v1/foo/bar?')
        query_params_str = url.split('?')[1]
        query_params = query_params_str.split('&')
        assert 'page=2' in query_params
        assert 'per_page=20' in query_params

    def test_url_paginator_escape(self):
        url = routes.url('/route', pagination={'foo&bar': 'I love Python'})
        query_params_str = url.split('?')[1]
        assert query_params_str == 'foo%26bar=I+love+Python'
