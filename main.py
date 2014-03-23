#!/usr/bin/env python

from codecorate import (invertibleGenerator, coroutine)


def sourceFromIterable(iterable, target):

    for elem in iterable:
        target.send(elem)

    target.close()


@invertibleGenerator(globals())
def genPairs(iterable):

    buf = []

    for elem in iterable:
        buf.append(elem)

        if len(buf) >= 2:
            yield tuple(buf)
            buf = []


@invertibleGenerator(globals())
def genPassthrough(iterable):
    for val in iterable:
        yield val


@coroutine
def coReceive():
    while True:
        val = (yield)
        print "Got %s" % str(val)


if __name__ == "__main__":

    print "Generators:"
    for val in genPassthrough(genPairs(xrange(0, 9))):
        print "Got %s" % str(val)

    print "Coroutines:"
    sourceFromIterable(xrange(0, 9),
                       genPairs.co(
                       genPassthrough.co(
                       coReceive())))