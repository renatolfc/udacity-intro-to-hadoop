#!/usr/bin/env python
# encoding: utf-8

"""Reducer module for solving the `Study Groups`_ problem.

.. _Study Groups: https://www.udacity.com/course/viewer#!/c-ud617/l-717558831/m-730138597

.. module:: study_groups_reducer
.. moduleauthor:: Renato L. F. Cunha <renato@renatocunha.com>
"""

from __future__ import print_function

import sys

# To make our reducers lives' easier, we want questions before the rest. {{{
QUESTION = 'A'
WHATEVER = 'B'
# }}}


def getData(line):
    """Basic sanity checking function.

    Makes sure a line is valid before outputting it to the mapper by doing some
    basic sanity checks.

    :line: The line to be validated.
    :returns: The data in the format expected if it is valid. None otherwise.
    """
    data = line.strip().split('\t')

    # Our mapper outputs three columns. Anything different than that can be
    # considered corrupt
    if len(data) != 3:
        return None

    # In the format we expect
    node, nodeType, author = data

    return node, True if nodeType == QUESTION else False, author


def output(thread, authors):
    """Outputs the information this reducer has consolidated.

    :thread: The thread id we're outputting information about.
    :authors: The list of authors that has contributed to this thread.
    :returns: None.

    """
    print('{0}\t{1}'.format(thread, ','.join(authors)))


def reducer():
    """Reducer function.

    :returns: Nothing. Writes to standard output.

    """

    # Initialize the reducer. Authors hold the list of authors for the current
    # thread.
    authors = []
    # Holds the thread id (the node id of the question that originated this
    # thread)
    lastThread = None
    for line in sys.stdin:
        data = getData(line)
        if data is None:
            continue

        # Unpack our data. See `getData()`
        thread, newThread, author = data

        # The line we just read starts a new thread. We must output the
        # information about the previous one before continuing.
        if thread != lastThread:
            # A weird thing can happen here. If the data from the database is
            # inconsistent, we can have a question without an originating
            # thread. What now? My take would be to ignore these altogether,
            # but there is at least one thread (8001899) which has no question
            # but has answers. Therefore, since we *do* have a parent id, we
            # will print it.

            # No point in printing info about a thread that doesn't exist
            if lastThread is not None:
                output(lastThread, authors)
                authors = []

        authors.append(author)

        lastThread = thread

    # Leftover state from the loop
    output(lastThread, authors)


if __name__ == '__main__':
    reducer()
