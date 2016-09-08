"""
PayPlug python library setup tool.
"""
import sys
import io
from os import path

from setuptools import setup, find_packages
from setuptools.command.test import test

current_path = path.abspath(path.dirname(__file__))
with io.open(path.join(current_path, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

__version__ = 'unknown'
with io.open(path.join(current_path, 'payplug', '__version__.py'), encoding='utf-8') as f:
    for line in f:
        if not line.startswith('#'):
            exec(line)


class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = ['payplug']

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
    version=__version__,
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

    install_requires=['requests>=1.0.1,<3.0', 'six>=1.4.0', 'pyOpenSSL>=0.15'],
    tests_require=['pytest>=2.7.0', 'mock>=1.0.1,<2.0', 'six>=1.7.0'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'payplug': ['certs/cacert.pem'],
    },
    cmdclass={'test': PyTest},
)
