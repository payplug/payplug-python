# -*- coding: utf-8 -*-
"""
Configuration parameters.

payplug.config.secret_key:
    Your secret key. This can either be a string or None.
    You should always prefer leaving it to None and setting it using set_secret_key function:
        >>> import payplug
        >>> payplug.set_secret_key('your_secret_key')

payplug.config.cacert_path:
    Path to CA root certificates.
"""
import os

CACERT_PATH = os.path.join(os.path.dirname(__file__), 'certs', 'cacert.pem')

secret_key = None
api_version = None
