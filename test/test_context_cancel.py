#!/usr/bin/env python3

import uuid
import threading
import time
import logging

from context import ContextWithCancel, cancel_context


logging.basicConfig(level=logging.DEBUG)


def test_thread(id: str):
    with ContextWithCancel(id, True):
        while True:
            print("Worker runs")
            time.sleep(1)

def run_tests():
    ctx_id = str(uuid.uuid4())
    worker = threading.Thread(target= test_thread, args=(ctx_id,))
    worker.start()

    time.sleep(1)
    cancel_context(ctx_id)

if __name__ == "__main__":
    run_tests()