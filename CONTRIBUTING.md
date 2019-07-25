# Contributing

If you want to contribute to this project, please submit an issue describing your proposed change. We will respond to you as soon as we can.

This project requires Python 3, all of the initial development has been done using Python 3.7.2

If you want to work on that change, fork this Github repo and clone the fork locally
```sh
git clone https://github.com/<your_username>/pywsitest
cd pywsitest
```

Set up a virtual environment and install all dependencies
```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

To run unit tests
```sh
python -m unittest
```

In order for changes to be accepted, Grid Smarter Cities requires that all code pass a series of tests

Firstly we require all unit tests to be passing, and that test coverage is 100%
```sh
coverage run --branch --source='.' -m unittest
coverage report -m --fail-under=100 --omit=*/__init__.py,tests/*,setup.py,env/*
```

We require all code to adhere to our linting style as defined in [pylintrc](https://github.com/gridsmartercities/pywsitest/blob/master/pylintrc)
```sh
prospector
```

And lastly that [Bandit](https://pypi.org/project/bandit/) security checks pass
```sh
bandit -r . -x env/
```

Once the changes are finished and the criteria for merging are met, simply create a pull request all it'll be reviewed as soon as possible

Thanks for contributing!