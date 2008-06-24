#! /usr/bin/env python

"""responsible for loading and keeping all the composite widgets"""

import xml.dom.minidom as minidom
import os
import goo.parser

file_path = ""
COMPOSITES = {}

def get(tagname):
    """load composite widget

    load the first widget in the file registered under tagname
    """
    if tagname not in COMPOSITES:
        raise ParseError("encountered invalid tag: '%s'" % node.tagName)

    xml_file = os.path.join(file_path, COMPOSITES[tagname])
    dom = minidom.parse(xml_file)
    node = dom.documentElement.firstChild

    while node.nodeType == 3:
        node = node.nextSibling

    #recurse back into get_widget until we find some built-in widgets
    return goo.parser.get_widget(node)[0], node

def register(name, xml_file):
    """register new composite tag

    register a new composite tag, so it will be recognised if it appears in
    your files.
    """
    for index, arg in enumerate((name, xml_file)):
        if not isinstance(arg, basestring):
            raise TypeError("register() argument %d must be string not %s" % (index, type(arg).__name__))
        elif arg == "":
            raise ValueError("invalid argument %d for register: '%s'" % (index, arg))

    COMPOSITES[name] = xml_file
