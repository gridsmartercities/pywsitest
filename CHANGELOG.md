## Version 0.1
First published bersion of pywsitest on PyPI  
At this point, users can setup a test with:
- A URL and query parameters
- Expected responses
- Messages to send on connect
- Messages that are triggered from a response
- Configurable timeouts
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