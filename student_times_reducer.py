#!/usr/bin/env python
# encoding: utf-8

"""Reducer module for solving the `Student Times`_ problem.

.. _Student Times: https://www.udacity.com/course/viewer#!/c-ud617/l-717558831/m-713019075

.. module:: student_times_reducer
.. moduleauthor:: Renato L. F. Cunha <renato@renatocunha.com>
"""

from __future__ import print_function

import sys

def increment(postHours, hour):
    """Increments the number of times a user has posted in a giver hour.
    
    :postHours: A list that represents the state of posts for a given user.
    :hour: The hour that is to be incremented.

    :returns: Nothing.
    """
    postHours[hour % 24] += 1


def emptyHours():
    """Returns an empty list of hours."""
    return [0] * 24


def getMatchingIndices(iterable, value):
    """Returns a list containing the indices in an iterable that match a value.
    
    :iterable: The iterable to iterate on.
    :value: The value to be search on the iterable.
    :returns: A list with all the matching indices.
    """
    return [i for i, e in enumerate(iterable) if e == value]


def output(author, postHours):
    """Outputs the hours on which a user most usually posts.

    :author: The author whose hours "belong" to.
    :postHours: The state about this author.
    """
    maximum = max(postHours)
    for hour in getMatchingIndices(postHours, maximum):
        print('{0}\t{1}'.format(author, hour))


def getData(line):
    """Basic sanity checking function.
    
    Makes sure a line is valid before outputting it to the mapper by doing some
    basic sanity checks.

    :line: The line to be validated.
    :returns: The data in the format expected if it is valid. None otherwise.
    """
    data = line.strip().split('\t')

    # Our mapper outputs two columns. Anything different than that can be
    # considered corrupt
    if len(data) != 2:
        return None

    # In the format we expect
    author, hour = data

    try:
        hour = int(hour)
    except ValueError:
        # This is not an hour. :'(
        return None

    return author, hour

def reducer():
    """Reducer function.

    :returns: Nothing. Writes to standard output.
    """

    # Init the reducer
    lastAuthor = '-1'
    postHours = emptyHours()

    for line in sys.stdin:
        data = getData(line)
        if data is None:
            continue
        author, hour = data

        # The line we just read belong to a different author. We must output
        # the information about the previous one and initialize the state for
        # the new one.
        if author != lastAuthor:
            # We don't want to output data because the line we read is
            # different from the initialization data.
            if lastAuthor != '-1':
                output(lastAuthor, postHours)
                postHours = emptyHours()
            # Increment the counter for the current hour
            increment(postHours, hour)

        lastAuthor = author

    # We exited the loop, but we still have state stored. Output it.
    output(author, postHours)


if __name__ == '__main__':
    reducer()
