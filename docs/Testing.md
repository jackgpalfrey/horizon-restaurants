# Testing

## Unit Tests

Unit tests are written using the [pytest](https://docs.pytest.org/en/latest/) framework. All unit tests should be placed in the tests/ directory. The tests can be run as described in [[Docker]]. When creating pull requests (See [[Git]]) the tests will be run automatically and if they fail it will stop the pull request from being merged.

All unit tests should be grouped together in files following the naming convention `test_*.py`. The test functions should then be named `test_*`. This is so that pytest can automatically find and run the tests.