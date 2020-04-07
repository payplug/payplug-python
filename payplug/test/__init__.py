# -*- coding: utf-8 -*-
import payplug


class TestBase:
    def setup_method(self, method):
        payplug.secret_key = None
        payplug.api_version = None
