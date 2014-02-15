#!/usr/bin/env python
# encoding: utf-8

"""Helper code for the Final Project of the "Intro to Hadoop and MapReduce"
course.

.. modeule:: common
.. moduleauthor:: Renato L. F. Cunha <renato@renatocunha.com>
"""

NODE_FIELDS = [
    "id",
    "title",
    "tagnames",
    "author_id",
    "body",
    "node_type",
    "parent_id",
    "abs_parent_id",
    "added_at",
    "score",
    "state_string",
    "last_edited_id",
    "last_activity_by_id",
    "last_activity_at",
    "active_revision_id",
    "extra",
    "extra_ref_id",
    "extra_count",
    "marked"
]


def getFieldNumber(fieldName):
    """Given a node field's name, returns its index in which it would appear.

    :fieldName: The name of the field we're searching.
    :returns: The field's index when found, -1 otherwise.

    """
    try:
        return NODE_FIELDS.index(fieldName)
    except ValueError:
        return -1


def getField(line, fieldName):
    """Given a line read from the input file and a field name, return that
    field's value.

    :line: The line just read.
    :fieldName: The name of the field the user wants.
    :returns: The field's value when data is found, None otherwise.
    """
    index = getFieldNumber(fieldName)
    if index < 0:
        return None
    return line[index]


def isValidNodeLine(line):
    """Does basic sanity-checking on a line from the forum node "table".

    :line: The line to be tested.
    :returns: True if it looks like the line is good. False otherwise.
    """

    # The line must have the same number of fields that we're expecting
    if len(line) != len(NODE_FIELDS):
        return False

    try:
        # If "id" is not numeric, this line is probably the file's header,
        # or the data is corrupt.
        int(getField(line, 'id'))
    except ValueError:
        # Either way, we don't want it
        return False

    # Okay, the data looks fine
    return True
