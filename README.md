[<img align="right" alt="Grid Smarter Cities" src="https://s3.eu-west-2.amazonaws.com/open-source-resources/grid_smarter_cities_small.png">](https://www.gridsmartercities.com/)

![Build Status](https://codebuild.eu-west-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiSitwRmNUcHk2VzN2VS8rMHdUS2hoNzZCQUdCME1VV0RkeWEwTmZyVUxOWUdXR2hMTzVUVWIvLzJ5ZFR2SWo5OHhtSm55TFc4SjZvcGhNcndNT1lDbEdRPSIsIml2UGFyYW1ldGVyU3BlYyI6Ik9SV0g1Tm1FMUVERW9RSzciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# pywsitest - PYthon WebSocket Integration TESTer
A python API to assist with automated websocket integration testing.

## Installation
```
pip install pywsitest
```

## Package contents

## Examples
Testing a reponse with a body is received on connection to a websocket:
```py
from pywsitest import WSTest, WSResponse
...
ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body")
    )
)

# {
#     "body": "Hello, world!"
# }

await ws_test.run()

assert ws_test.is_complete()
```

Testing a more complex set of responses is received on connection to a websocket:
```py
from pywsitest import WSTest, WSResponse
...
ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("type", "on_connect")
        .with_attribute("body")
    )
    .with_response(
        WSResponse()
        .with_attribute("type", "notification")
        .with_attribute("body", {"message": "1 new message"})
    )
)

# {
#     "type": "on_connect",
#     "body": {
#         "first": 123,
#         "second": 456
#     }
# }
#
# {
#     "type": "notification",
#     "body": {
#         "message": "1 new message"
#     }
# }

await ws_test.run()

assert ws_test.is_complete()
```

## Documentation

##Links