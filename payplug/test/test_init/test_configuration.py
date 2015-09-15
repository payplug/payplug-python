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
