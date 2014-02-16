#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import sys
import csv

from common import getField, isValidNodeLine

# To make our reducers lives' easier, we want questions before answers. {{{
QUESTION = 'A'
ANSWER = 'B'
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

        # The fields we're interested in. For questions, we obviously want
        # their ids to be output, along with their body lengths. For answers,
        # we actually want to output the value of "parent_id", and the reason
        # for that is that we want answers to be grouped together with the
        # questions that caused them to be. The node_type is used to decide if
        # this is a question or an answer. Comments should be ignored.

        node = getField(line, 'id')
        nodeType = getField(line, 'node_type')
        parent = getField(line, 'abs_parent_id')
        body = getField(line, 'body')

        # If any of the fields we're interested in is None, then it is no good
        # for us. Drop this line altogether.
        if any(map(lambda x: x == None, (node, nodeType, parent, body))):
            continue

        # Data output, as announced by the comments above
        # NOTE: We're assuming neither questions nor answers can be empty.
        # We're hoping that the forum software prevented that from happening.
        # The only reason this comment is made here is because it looks like,
        # from the database dump, that empty values get filled with the "\N"
        # string, which has a length of two. This could be improved, but
        # I believe this happening would be quite unlikely.
        if nodeType == 'question':
            print('{0}\t{1}\t{2}'.format(node, QUESTION, len(body)))
        elif nodeType == 'answer':
            print('{0}\t{1}\t{2}'.format(parent, ANSWER, len(body)))
        else:
            # We don't care about it.
            continue

if __name__ == '__main__':
    mapper()

