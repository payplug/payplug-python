# -*- coding: utf-8 -*-
import py.test
from payplug import config, exceptions
from payplug.test import TestBase


class TestSecretKey(TestBase):
    def test_invalid_secret_key(self):
        import payplug
        with py.test.raises(exceptions.ConfigurationError) as excinfo:
            payplug.set_secret_key(None)
        assert 'Expected string value for token.' == str(excinfo.value)
        assert config.secret_key is None

    def test_secret_key_set(self):
        import payplug
        assert config.secret_key is None
        payplug.set_secret_key('a_secret_key')
        assert config.secret_key == 'a_secret_key'

class TestApiVersionKey(TestBase):
    def test_invalid_api_version(self):
        import payplug
        with py.test.raises(exceptions.ConfigurationError) as excinfo:
            payplug.set_api_version(None)
        assert 'Expected string value for version.' == str(excinfo.value)
        assert config.api_version is None

    def test_secret_api_version(self):
        import payplug
        assert config.api_version is None
        payplug.set_api_version('my_api_version')
        assert config.api_version == 'my_api_version'
