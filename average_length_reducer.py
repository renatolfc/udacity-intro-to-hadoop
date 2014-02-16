#!/usr/bin/env python
# encoding: utf-8

"""Reducer module for solving the `Post and Answer Length`_ problem.

.. _Post and Answer Length: https://www.udacity.com/course/viewer#!/c-ud617/l-717558831/m-700668970

.. module:: average_length_reducer
.. moduleauthor:: Renato L. F. Cunha <renato@renatocunha.com>
"""

from __future__ import print_function
from __future__ import division # Float division by default

import sys

# To make our reducers lives' easier, we want questions before answers. {{{
QUESTION = 'A'
ANSWER = 'B'
# }}}

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
    if len(data) != 3:
        return None

    # In the format we expect
    node, nodeType, length = data

    try:
        length = int(length)
    except ValueError:
        # This is not a body length. :'(
        return None

    if nodeType == QUESTION:
        return node, True, length
    elif nodeType == ANSWER:
        return node, False, length
    else:
        return None


def getQuestionLength(nodeInfo):
    "Extracts the question length from a nodeInfo."
    return nodeInfo[0]


def getAverageAnswerLength(nodeInfo):
    "Extracts the average answer length from a nodeInfo."
    try:
        return nodeInfo[1] / nodeInfo[2]
    except ZeroDivisionError:
        # There will be cases in which a post has no answers. Clearly, in this
        # case, the average answer length cannot be positive. Likewise,
        # negative values make no sense. So zero is the only sane output
        return 0


def output(node, nodeInfo):
    """Outputs the information this reducer has consolidated.

    :node: The node id we're outputting information about.
    :nodeInfo: The node's statistics: question length, total answer length and
               amount of answers.
    :returns: None.

    """
    print('{0}\t{1}\t{2}'.format(node,
                                 getQuestionLength(nodeInfo),
                                 getAverageAnswerLength(nodeInfo)
                                ))


def emptyNodeInfo():
    'Returns a completely new node information "structure".'
    return [0] * 3


def update(nodeInfo, isQuestion, length):
    "Updates nodeInfo with the information we just read."

    if isQuestion:
        nodeInfo[0] = length
    else:
        nodeInfo[1] += length
        nodeInfo[2] += 1


def reducer():
    """Reducer function.

    :returns: Nothing. Writes to standard output.
    """

    # Init the reducer
    lastNode = '-1'
    nodeInfo = emptyNodeInfo()

    for line in sys.stdin:
        data = getData(line)
        if data is None:
            continue

        node, isQuestion, length = data

        # The line we just read belong to a different node. We must output
        # the information about the previous one and initialize the state for
        # the new one.
        if node != lastNode:
            # We don't want to output data just because the line we read is
            # different from the initialization data.
            if lastNode != '-1':
                output(lastNode, nodeInfo)
                nodeInfo = emptyNodeInfo()

        # Update the information about the current node
        update(nodeInfo, isQuestion, length)

        lastNode = node

    # We exited the loop, but we still have state stored. Output it.
    output(lastNode, nodeInfo)


if __name__ == '__main__':
    reducer()
