# AlertOver-Python
A python package for [AlertOver](https://www.alertover.com/).
<br/>
Push messages form your code to your devices in a minute.

## Features:
Both synchronized and asynchronized support.
<br/>
Integration with python built-in logger.

## Install:
pip install 

## Dependency:
Python >= 3.5
<br/>
request
<br/>
aiohttp

## Usage:

Simple case:

```python
from alertover import send
send("your_source_id", "your_receiver_group_id",
        title="AlertOverTest",
        urgent=False,
        sound="system",
        content="Hello world",
        url="example.com")
```

Or more graceful:
```python
from alertover import Session
with Session("your_source_id",
    "your_source_id") as session:
        session.send(title="AlertOverTest",
                         urgent=False,
                         sound="system",
                         content="Hello world",
                         url="example.com")
```

Integration with python built-in logging system:
```python
import logging
from alertover import AlertOverHandler
logger  = logging.getLogger("test")
hdlr = AlertOverHandler("your_source_id",
                 "your_receiver_group_id", level=logging.ERROR)
                 
logger.addHandler(hdlr)

logger.exception("From AlertOverHandler.",
    extra={"title": "AlertOverHandlerTest"})
```

Integration with asynchronize framework:
```python
import alertover.async as aao
```

