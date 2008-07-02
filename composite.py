#! /usr/bin/env python

"""responsible for loading and keeping all the composite widgets"""

import xml.dom.minidom as minidom
import os
import goo.parser, goo.containers

file_path = ""

class Composite(goo.containers.Sizer):
    """Responsible for loading widgets from xml files and using them as children"""

    def __init__(self, parent, children, source, **attributes):
        """initialize this composite widget"""
        self.childnodes = children
        children = goo.parser.get_root(os.path.join(file_path, source)).childNodes
        for node in children:
            if node.nodeType not in (3, 8):
                new_attributes = goo.parser.get_attributes(node)
                new_attributes.update(attributes)
                print new_attributes
                break
        goo.containers.Sizer.__init__(self, parent, children, **new_attributes)

class Content(object):
    """return tag from original file with type and name

    this tag is found in composite files. It is replaced by a tag (whose tagname must be equal to the type attribute)
    from one of the child nodes of the composite tag, as used in the file importing the composite file.
    note that content tags are replaced with the original tags in order, e.g. the first content tag in the composite file is
    replaced with the first tag in the original file.
    """
    def __new__(cls, parent, tagtype=None, **attributes):
        composite = cls.find_composite(parent)
        node = cls.find_firstnode(composite)
        if node.tagName != tagtype:
            raise RuntimeError("tag to replace Content tag has wrong type: '%s'" % node.tagName)

        widget = goo.parser.get_widget(node)
        new_attributes = goo.parser.get_attributes(node)
        attributes.update(new_attributes)

        node.parentNode.removeChild(node)

        if node.hasChildNodes():
            return widget(parent, node.childNodes, **attributes)
        else:
            return widget(parent, **attributes)

    @staticmethod
    def find_composite(parent):
        """find the composite method in the hierarchy"""
        while not isinstance(parent, Composite):
            parent = parent.parent
            if isinstance(parent, goo.NullParent):
                raise RuntimeError("Content tag used in non-composite file")
        return parent

    @staticmethod
    def find_firstnode(parent):
        """find the first non-text node in the node list"""
        for node in parent.childnodes:
            if node.nodeType != 3:
                return node
