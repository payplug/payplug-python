Welcome to PayPlug e-commerce library's documentation!
======================================================

This is the documentation of PayPlug's Python library. It is designed to help developers to use PayPlug as
payment solution in a simple, yet robust way.

Prerequisites
-------------

PayPlug's library relies on **python-requests>=1.0.1** to perform HTTP requests and requires **OpenSSL** to secure
transactions. You also need either a **Python 2** newer than **Python 2.6** or a **Python 3** newer than **Python 3.1**.
To ensure **Python 2** and **Python 3** compatibility, this library also depends on **six>=1.4.0**.

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

If everything run without error, congratulations. You installed PayPlug python library! You're ready to create your
first payment.

Usage
-----

Here's how simple it is to create a payment request:

.. sourcecode :: python

    payment_data = {
        'amount': 3300,
        'currency': 'EUR',
        'customer': {
            'email': 'john.watson@example.net',
            'first_name': 'John',
            'last_name': 'Watson',
        },
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
