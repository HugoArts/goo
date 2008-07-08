#! /usr/bin/env python

"""parser.py: parse the xml documents into actual GUI elements"""

import xml.dom.minidom as minidom
import pygame
import gunge.mv
import goo

PARSE_ALL = 0


class ParseError(Exception):
    """Raised when an error occurs while parsing an xml document"""
    def __init__(self, msg, filename):
        Exception.__init__(self, msg)
        self.filename = filename

    def __str__(self):
        return self.message + " (file: %s)" % self.filename


def load_xml(filename, ids=None):
    """load an xml file and return the resulting widget(s)

    this loads the filename given, turns it into a dom object, and then hands it over to the 
    parse function, which builds a widget from it. the widget is then returned. If the 
    document contains multiple widgets, the caller can specify which ones to build with a 
    list of IDs, or pass in goo.parser.PARSE_ALL to build all widgets. A list of the built
    widgets is returned. If no ids argument is given, only the first widget is built.
    """
    root = get_root(filename)

    if ids is None:
        return parse_firstchild(root)
    elif ids is PARSE_ALL:
        return parse_all(root)
    else:
        return parse_ids(root, ids)

def get_root(filename):
    """get the root element of an xml document"""
    dom = minidom.parse(filename)
    root = dom.documentElement
    if root.tagName != "gamegoo":
        raise ParseError("Invalid GameGoo XML document: invalid root node", filename)
    return root

def parse_firstchild(rootnode):
    """parse the first child of some node"""
    node = rootnode.firstChild
    while node.nodeType == 3:
        node = node.nextSibling
    widget = parse(node)
    widget.arrange(pygame.Rect(10, 10, 0, 0))
    return widget

def parse_all(rootnode):
    """parse all children of a node"""
    widgets = tuple(parse(node) for node in rootnode.childNodes if nodetype != 3)
    for widget in widgets:
        widget.arrange(pygame.Rect(10, 10, 0, 0))
    return widgets

def parse_ids(rootnode, id_list):
    """parse all children of a node with an id in id_list"""
    doc = rootnode.ownerDocument
    widgets = tuple(parse(doc.getElementbyId(id_)) for id_ in id_list)
    for widget in widgets:
        widget.arrange(pygame.Rect(10, 10, 0, 0))
    return widgets

def parse(node, parent=None):
    """Parse a DOM node and create a widget from it

    takes an xml DOM node and creates a widget from it.
    The node is attached to the parent, if specified. Otherwise, the special NullParent is used.
    the nodes' children are handed to the created widget to also be parsed.
    """
    if parent is None:
        parent = goo.NullParent()
    widget = get_widget(node)

    if issubclass(widget, goo.containers.Container):
        widget = widget(parent, node.childNodes, **get_attributes(node))
    else:
        widget = widget(parent, **get_attributes(node))

    if widget is not None:
        gunge.mv.ModelView.get_global().add(widget)
    return widget

def get_widget(node):
    """Retrieve a widget for a certain node.
    
    Every node has an associated widget that must be built. This function fetches
    the relevant class to do so. It uses the string of the tagname to retrieve the right class.
    """
    #the widget could be located in one of several modules. We'll have to try them all
    for module in (goo.controls, goo.containers, goo.composite):
        try:
            return getattr(module, node.tagName)
        except AttributeError:
            continue
    #not a registered widget, error
    raise ParseError("encountered invalid tag: '%s'" % node.tagName)

def get_attributes(node):
    """retrieve a dictionary of the attributes for a node"""
    attr_map = node.attributes
    attributes = (attr_map.item(i) for i in range(attr_map.length))
    return dict((str(attr.name), attr.value) for attr in attributes)
