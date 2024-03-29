1.4.0
-----
- Add OneyPaymentSimulation class to handle the /oney_payment_simulations API endpoint

1.3.1
-----
- Add missing `Billing` and `Shipping` entities to payment resource

1.3.0
-----
- Add AccountingReport class to handle the new /accounting\_reports API endpoint

1.2.2
-----
- Add API version setting
- Fix tests
- Move CI to Github Actions

1.2.1
-----
- Require pyOpenSSL>=0.15 to prevent random failures.
- Log more errors in case of request failure.

1.2.0
-----

- **NEW**: Support for Customers and Cards. (see official documentation)
- **NEW**: Add ability to abort payment objects.

  ```
  payment.abort()
  ```

- **NEW**: This library is now under MIT Licence (Issue #4).
- Minor fixes in tests.
- Add this changelog.
