"""
PayPlug python library setup tool.
"""
import sys
import io
import re
from os import path

from setuptools import setup, find_packages
from setuptools.command.test import test

current_path = path.abspath(path.dirname(__file__))
with io.open(path.join(current_path, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

version = 'unknown'
version_matcher = re.compile('^__version__\s?=\s?[\'"](.*)[\'"]$')
with io.open(path.join(current_path, 'payplug', '__version__.py'), encoding='utf-8') as f:
    for line in f:
        result = version_matcher.match(line)
        if result:
            version = result.group(1)


class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='payplug',
    version=version,
    description='PayPlug payment solution',
    long_description=long_description,
    url='https://github.com/payplug/payplug-python/releases',
    author='PayPlug',
    author_email='support@payplug.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries :: Python Modules',

        "Operating System :: OS Independent",

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    keywords='payplug payment integration api',

    packages=find_packages(exclude=['*.test*']),

    install_requires=['requests>=1.0.1,<3.0', 'six>=1.4.0'],
    tests_require=['pytest>=2.7.0', 'mock>=1.0.1', 'six>=1.7.0'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'payplug': ['certs/cacert.pem'],
    },
    cmdclass={'test': PyTest},
)
