# Contributing

If you want to contribute to this project, please submit an issue describing your proposed change. We will respond to you as soon as we can.
 
If you want to work on that change, fork this Github repo and clone the fork locally.

- you run [__Bandit__](https://pypi.org/project/bandit/) for security checking and all checks are passing:

`bandit -r .`
 
- you run [__Prospector__](https://pypi.org/project/prospector/) for code analysis and all checks are passing:

`prospector`

- you run [__Coverage__](https://pypi.org/project/coverage/) and all unit tests are passing:

`coverage run --branch --source='.' -m unittest`

- you have 100% unit test coverage:

`coverage report -m --fail-under=100 --omit=*/__init__.py,tests/*,setup.py,examples/test_examples.py`

Thanks for contributing!