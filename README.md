[<img align="right" alt="Grid Smarter Cities" src="https://s3.eu-west-2.amazonaws.com/open-source-resources/grid_smarter_cities_small.png">](https://www.gridsmartercities.com/)

# pywsitest
A python API to assist with automated websocket integration testing.

## Installation
```
pip install pyswitest
```

## Package contents

## Examples
```py
from pywsitest import WSTest, WSResponse
...
ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body", "Hello, world!")
    )
)

await ws_test.run()

assert ws_test.is_complete()
print(ws_test.received_json)
```

## Documentation

##Links