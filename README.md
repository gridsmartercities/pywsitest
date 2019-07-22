[<img align="right" alt="Grid Smarter Cities" src="https://s3.eu-west-2.amazonaws.com/open-source-resources/grid_smarter_cities_small.png">](https://www.gridsmartercities.com/)

![Build Status](https://codebuild.eu-west-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiSitwRmNUcHk2VzN2VS8rMHdUS2hoNzZCQUdCME1VV0RkeWEwTmZyVUxOWUdXR2hMTzVUVWIvLzJ5ZFR2SWo5OHhtSm55TFc4SjZvcGhNcndNT1lDbEdRPSIsIml2UGFyYW1ldGVyU3BlYyI6Ik9SV0g1Tm1FMUVERW9RSzciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/pywsitest.svg?color=brightgreen)](https://pypi.org/project/pywsitest)

# pywsitest
## PYthon WebSocket Integration TESTing framework

A python API to assist with automated websocket integration testing



## Installation
```
pip install pywsitest
```

## Package contents
### [WSTest](https://github.com/gridsmartercities/pywsitest/blob/master/pywsitest/ws_test.py)
WSTest is the main test running class in pywsitest. It currently has the following methods:
- **with_parameter**: add a query parameter to the connection
- **with_response**: add an expected response to the test runner
- **with_message**: add a message for the test runner to send on connection
- **with_response_timeout**: set the timeout in seconds for the test runner to wait for a response from the websocket
- **with_message_timeout**: set the timeout in seconds for the test runner to wait while trying to send a message to the websocket
- **with_test_timeout**: set the timeout in seconds for the test runner to run for
- **run**: asyncronously run the test runner, sending all messages and listening for responses
- **is_complete**: check whether all expected responses have been received and messages have been sent

### [WSResponse](https://github.com/gridsmartercities/pywsitest/blob/master/pywsitest/ws_response.py)
WSResponse is a class to represent an expected response from the websocket
- **with_attribute**: add an attribute to check an incoming response against
- **with_trigger**: add a message to trigger when a response matching this instance has been received
- **is_match**: check whether a received response matches the attributes of this instance

### [WSMessage](https://github.com/gridsmartercities/pywsitest/blob/master/pywsitest/ws_message.py)
WSMessage is a class to represent a message to send to the websocket
- **with_attribute**: add an attribute to the message to be sent to the websocket host

## Examples
Testing a reponse with a body is received on connection to a websocket:
```py
from pywsitest import WSTest, WSResponse

ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Testing a more complex set of responses and messages:
```py
from pywsitest import WSTest, WSResponse, WSMessage

ws_test = (
    WSTest("wss://example.com")
    .with_parameter("Authorization", "eyJra...")
    .with_response_timeout(15) # 15 seconds
    .with_message_timeout(7.5)
    .with_test_timeout(45)
    .with_message(
        WSMessage()
        .with_attribute("type", "connect")
        .with_attribute("body", {"chatroom": "general"})
    )
    .with_response(
        WSResponse()
        .with_attribute("type", "connected")
        .with_trigger(
            WSMessage()
            .with_attribute("type", "message")
            .with_attribute("body", "Hello, world!")
        )
    )
    .with_response(
        WSResponse()
        .with_attribute("type", "message")
        .with_attribute("body", "Hello, world!")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

## Documentation
Users can get the docstring help by running:
```py
from pywsitest import WSTest
help(WSTest.with_response)
```

## Links
- [Github](https://github.com/gridsmartercities/pywsitest)
- [PyPI](https://pypi.org/project/pywsitest)
- [Test PyPI](https://test.pypi.org/project/pywsitest)