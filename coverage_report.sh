#!/bin/bash

coverage run --branch --source='.' -m unittest
coverage report -m --fail-under=100 --omit=*/__init__.py,tests/*,env/*