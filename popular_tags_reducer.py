#!/usr/bin/env python
# encoding: utf-8

"""Reducer module for solving the `Top Tags`_ problem.

.. _Top Tags: https://www.udacity.com/course/viewer#!/c-ud617/l-717558831/m-700468914

.. module:: popular_tags_reducer
.. moduleauthor:: Renato L. F. Cunha <renato@renatocunha.com>
"""

from __future__ import print_function

import sys
import heapq

TOP_N_TAGS = 10

def getData(line):
    "Basic sanity checking function. Gets the data for this reducer."

    data = line.strip().split('\t')

    # Our mapper outputs two columns. Anything different than that can be
    # considered corrupt
    if len(data) != 2:
        return None

    tag, amount = data

    try:
        amount = int(amount)
    except ValueError:
        # This is not an amount. Oops?
        return None

    return tag, amount


def update(topN, tag, amount):
    """Updates the topN heap with the new tag.

    :topN: The heap we're maintaining.
    :tag: The tag to be added.
    :amount: The number of times this tag appears.
    :returns: None

    """
    heapq.heappush(topN, (amount, tag))
    if len(topN) > TOP_N_TAGS:
        heapq.heappop(topN)


def output(topN):
    """Outputs the TOP N fields in the heap in ascending order.

    :topN: The heap to be iterated on.
    :returns: None

    """
    for elem in heapq.nsmallest(TOP_N_TAGS, topN):
        print('{0}\t{1}'.format(elem[1], elem[0]))


def reducer():
    """Reducer function.

    :returns: Nothing. Writes to standard output.
    """

    # Init the reducer
    topN = []
    lastTag = None
    lastAmount = 0
    for line in sys.stdin:
        data = getData(line)
        if data is None:
            continue

        tag, amount = data

        # If the line we just read belong to a different node, then we can add
        # this tag to our heap. If the heap became larger than the top N fields
        # we want, we will truncate it.
        if tag != lastTag:
            # It only makes sense to add the last tag to the heap if we had
            # info about it before. In other words, if this is the first tag,
            # there's no need to add anything to the heap yet.
            if lastTag is not None:
                update(topN, lastTag, amount)
                lastAmount = 0

        lastAmount += amount
        lastTag = tag

    # We exited the loop with remaining state. Update it.
    update(topN, lastTag, amount)

    # And now we have our top 10 (in a bounded amount of memory! \o/)
    output(topN)

if __name__ == '__main__':
    reducer()
