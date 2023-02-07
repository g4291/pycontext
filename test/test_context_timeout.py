#!/usr/bin/env python3

import time
import logging

from context import ContextWithTimeout


logging.basicConfig(level=logging.DEBUG)


def test_thread(timeout: float):
    with ContextWithTimeout(timeout, True):
        while True:
            print("Worker runs")
            time.sleep(1)

def run_tests():
    test_thread(3)

if __name__ == "__main__":
    run_tests()