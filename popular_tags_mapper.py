#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import sys
import csv

from common import getField, isValidNodeLine

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

    # NOTE: Funny thing happening here. We *cannot use* the top-N pattern
    # explained in class! Suppose the following example: we want the top 1
    # tag and we're using the top-N pattern presented in class. Now, suppose
    # we have two mappers and we actually have only two tags: tag1, and tag2.
    # Suppose our mappers see the following
    # Mapper 1:
    #   This gets all instances of tag1, which happen to be in this example,
    #   equal to 1000. BUT it also sees 400 instances of tag two.
    #   So, internally, we can have in mapper 1:
    #   tag1 = 1000
    #   tag2 = 400
    #
    # Mapper 2: Suppose mapper 2 sees only tag2 and its count is 900.
    # So, the internal list for mapper 2 will be:
    #   tag2 = 900
    #
    # Now, if we used the topN patter *as presented* in class, we'd be lost.
    # Our reducer would see as its input:
    #   tag1 = 1000
    #   tag2 = 900
    #
    # And it would output the incorrect top1 tag, tag1, with 1000 occurrences.
    #
    # If, instead, the mappers output all tags they saw, then the reducer would
    # have the chance to see this list:
    #   tag1 = 1000
    #   tag2 = 400
    #   tag2 = 900
    # Now it would be able to reduce correctly and output the top 1 tag, tag2.

    # We print everything we got.
    for tag in tagDict.items():
        print('%s\t%s' % tag)

    # Addendum:
    # Had I used the top N pattern, I would have defined a top-level function
    # called comparator like this:
    #
    # def comparator(a, b):
    #     "Custom comparator for sorting our list of tags."
    #
    #     # Equal keys have equal weights
    #     if a[1] == b[1]:
    #         return 0
    #     # Keys that appear more should come first
    #     elif a[1] < b[1]:
    #         return 1
    #     else:
    #         return -1
    #
    # Then, instead of printing all the tags, I would have defined
    # a mostFrequent list like this:
    #
    #  mostFrequent = sorted(list(tagDict.items()), cmp=comparator)
    #
    # Last, but not least, I would have printed the output like this:
    #
    # for tag in mostFrequent[:TOP_N_TAGS]:
    #   print('%s\t%s' % tag)


if __name__ == '__main__':
    mapper()

