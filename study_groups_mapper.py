#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import sys
import csv

from common import getField, isValidNodeLine

# To make our reducers lives' easier, we want questions before the rest. {{{
QUESTION = 'A'
WHATEVER = 'B'
# }}}

def mapper():
    """Mapper function.

    Input is read from sys.stdin and written to sys.stdout. Both streams can be
    overwritten if needed.

    :returns: Nothing. Writes to standard output.
    """

    # The input file is saved as a tab-separated file. The data itself comes from
    # http://content.udacity-data.com/course/hadoop/forum_data.tar.gz -- file
    # "forum_nodes.tsv".
    reader = csv.reader(sys.stdin, delimiter='\t')

    for line in reader:
        # Basic data sanity check
        if not isValidNodeLine(line):
            continue

        # The fields we're interested in. Question represent new threads,
        # comments & answers, posts to that thread. Hence, we need the node id
        # for questions and the parent id for answers / comments. We obviously
        # need the author id as well, so we can group that.
        node = getField(line, 'id')
        nodeType = getField(line, 'node_type')
        parent = getField(line, 'abs_parent_id')
        author = getField(line, 'author_id')

        # If any of the fields we're interested in is None, then it is no good
        # for us. Drop this line altogether.
        if any(map(lambda x: x == None, (node, nodeType, parent, author))):
            continue

        # Data output, as announced by the comments above
        if nodeType == 'question':
            print('{0}\t{1}\t{2}'.format(node, QUESTION, author))
        else:
            print('{0}\t{1}\t{2}'.format(parent, WHATEVER, author))


if __name__ == '__main__':
    mapper()

