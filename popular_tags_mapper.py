#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import sys
import csv

from common import getField, isValidNodeLine

TOP_N_TAGS = 10

def comparator(a, b):
    "Custom comparator for sorting our list of tags."

    # Equal keys have equal weights
    if a[1] == b[1]:
        return 0
    # Keys that appear more should come first
    elif a[1] < b[1]:
        return 1
    else:
        return -1

def mapper():
    """Mapper function.

    Input is read from sys.stdin and written to sys.stdout. Both streams can be
    overwritten if needed.

    :returns: Nothing. Writes to standard output.
    """

    # The input file is saved as a tab-separated file. The data itself comes
    # from http://content.udacity-data.com/course/hadoop/forum_data.tar.gz --
    # file "forum_nodes.tsv".
    reader = csv.reader(sys.stdin, delimiter='\t')

    # Dictionary that will hold the count of tags
    tagDict = {}
    for line in reader:
        # Basic data sanity check
        if not isValidNodeLine(line):
            continue

        tags = getField(line, 'tagnames')
        if tags is None:
            continue

        # Every tag gets added to the dictionary. If it doesn't exist yet, it
        # is added with value 1. Otherwise, its current value is incremented.
        tags = tags.split()
        for tag in tags:
            tagDict[tag] = tagDict.get(tag, 0) + 1

    # All tags, sorted by most frequent to least frequent
    mostFrequent = sorted(list(tagDict.items()), cmp=comparator)

    # We only want to output the 10 most frequent from *this* split.
    # Once the reducer(s) has(ve) the top 10 from all splits, it(they) will be
    # able to get the global top 10
    for tag in mostFrequent[:TOP_N_TAGS]:
        print('%s\t%s' % tag)

if __name__ == '__main__':
    mapper()

