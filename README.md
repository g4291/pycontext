# Pycontext

Context manager that allows long running functions to be interrupt with cancel call or with timeout

# Examples

## Cancel

```python

import time
import logging
from context import ContextWithCancel, cancel_context

logging.basicConfig(level=logging.DEBUG)

def test_thread(id: str):
    # block will be terminated when cancel_context(id) is called
    with ContextWithCancel(id, True):
        while True:
            print("Worker runs")
            time.sleep(1)


ctx_id = "some unique id"
worker = threading.Thread(target= test_thread, args=(ctx_id,))
worker.start()


time.sleep(1)

# cancel call
cancel_context(ctx_id)

```

## Timeout

```python

from context import ContextWithTimeout

logging.basicConfig(level=logging.DEBUG)

# block will be terminated after 3 seconds
with ContextWithTimeout(3):
    while True:
        print("Worker runs")
        time.sleep(1)


if __name__ == "__main__":
    run_tests()

```