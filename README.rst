Python library for the PayPlug API
==================================

.. image:: https://github.com/payplug/payplug-python/workflows/CI/badge.svg
   :target: https://github.com/payplug/payplug-python/actions
   :alt: CI Status

.. image:: https://img.shields.io/pypi/v/payplug.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/payplug/
   :alt: PyPi

This is the documentation of PayPlug's Python library. It is designed to help developers to use PayPlug as
payment solution in a simple, yet robust way.

You can create a PayPlug account at https://www.payplug.com.

Prerequisites
-------------

PayPlug's library relies on **python-requests>=1.0.1** to perform HTTP requests and requires **OpenSSL** to secure
transactions. You also need either a **Python 2.6+** or a **Python 3.3+**. The library is known to work with these
versions, pypy and pypy3. It may work on older versions or other Python implementations without warranty. If you use an
implementation that is not listed above, do not hesitate to let us known if it worked for you or not, so that we can
update this prerequisites.
To ensure **Python 2** and **Python 3** compatibility, this library also depends on **six>=1.4.0**.

Documentation
-------------
Please see https://www.payplug.com/docs/api for latest documentation.

Installation
------------

**Option 1 - Strongly preferred)** via PyPI:

.. code-block:: bash

    $ easy_install pip --upgrade
    $ pip install payplug


or simply add *payplug* as a dependency of your project.

**Option 2)** download as a tarball:

- Download the most recent stable tarball from the `download page`__
- Extract the tarball somewhere outside your project.
- *chdir* into the folder you've just extracted.
- Run the following commands:

.. code-block:: bash

    $ pip install --upgrade setuptools
    $ python setup.py install

__ https://github.com/payplug/payplug-python/releases

To get started, add the following piece of code to the header of your Python project:

.. sourcecode:: python

    import payplug

If everything runs without errors, congratulations. You installed PayPlug python library! You're ready to create your
first payment.

Usage
-----

Here's how simple it is to create a payment request:

.. sourcecode :: python

    payplug.set_api_version("2019-08-06")

    customer = {
        'email': 'john.watson@example.net',
        'first_name': 'John',
        'last_name': 'Watson',
        'address1': '221B Baker Street',
        'postcode': 'NW16XE',
        'city': 'London',
        'country': 'GB',
    }

    payment_data = {
        'amount': 3300,
        'currency': 'EUR',
        'billing': customer,
        'shipping': customer,
        'hosted_payment': {
            'return_url': 'https://www.example.net/success?id=42710',
            'cancel_url': 'https://www.example.net/cancel?id=42710',
        },
        'notification_url': 'https://www.example.net/notifications?id=42710',
        'metadata': {
            'customer_id': 42710,
        },
    }

    payment = payplug.Payment.create(**payment_data)

Go further:
-----------
Documentation:
++++++++++++++

https://www.payplug.com/docs/api/?python

Tests:
++++++
To run the tests for your specific configuration, run the following commands:

.. code-block:: bash

    $ easy_install pip --upgrade
    $ pip install --upgrade setuptools pbr
    $ python setup.py test

To run the tests under different configuration, you can use tox. It's recommended to use *pyenv* project to install
different python versions on the same system.

.. code-block:: bash

    $ pip install tox
    $ tox

You can also use *detox* to make the process even faster.

.. code-block:: bash

    $ pip install detox
    $ detox
