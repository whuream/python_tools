# encoding: utf-8
__author__ = 'tong'

import traceback
import json
import eventlet
import subprocess

eventlet.monkey_patch()

RETRY_COUNT = 10

TIMEOUT = 10


def time_limit(func, *args, **kwargs):
    trace = None
    for _ in range(RETRY_COUNT):
        try:
            with eventlet.Timeout(TIMEOUT):
                return func(*args, **kwargs)
        except eventlet.timeout.Timeout, e:
            trace = format_traceback()
        except:
            trace = format_traceback()

    ignore_exception = kwargs.get('ignore_exception')
    if not ignore_exception:
        raise Exception(
            "max retry count=%d, func=%s, argv=%s, trace=%s" % (RETRY_COUNT, func.__name__, (args, kwargs), trace))


def auto_retry(func, *args, **kwargs):
    trace = None
    for _ in range(RETRY_COUNT):
        try:
            return func(*args, **kwargs)
        except:
            trace = format_traceback()

    ignore_exception = kwargs.get('ignore_exception')
    if not ignore_exception:
        raise Exception(
            "max retry count=%d, func=%s, argv=%s, trace=%s" % (RETRY_COUNT, func.__name__, (args, kwargs), trace))


def format_traceback():
    trace = traceback.format_exc()
    return json.dumps(trace, ensure_ascii=False)


def print_traceback():
    print(json.dumps(traceback.format_exc(), ensure_ascii=False))


def exec_command(cmd):
    return subprocess.Popen(cmd, shell=True)


if __name__ == '__main__':
    def test(a):
        print(a)

    auto_retry(test, 1)
    time_limit(test, 2)

    exec_command("ls -al")