# -*- coding: utf-8 -*-
import re
from payplug.network import _get_python_version_string
from payplug.test import TestBase


class TestPythonVersion(TestBase):
    def test_python_version(self):
        re.match('\d\.\d\.\d', _get_python_version_string())
