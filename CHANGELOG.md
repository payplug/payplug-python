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
