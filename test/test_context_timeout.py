#!/usr/bin/env python3

import time
import logging

from context import ContextWithTimeout, ContextTimeoutError


logging.basicConfig(level=logging.DEBUG)


def run_tests():
    
    print("Test 1, timeout 3s, suppress exception")
    with ContextWithTimeout(3, True):
        while True:
            print("Worker runs")
            time.sleep(1)

    print("Test 2, timeout 3s, raise exception")
    try:
        with ContextWithTimeout(3):
            while True:
                print("Worker runs")
                time.sleep(1)
    except ContextTimeoutError as e:
        print("Timeout")

    print("Test 3, no timeout")
    with ContextWithTimeout(0):
        time.sleep(1)
        print("Bye")


if __name__ == "__main__":
    run_tests()