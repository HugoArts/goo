#! /usr/bin/env python

"""parser.py: parse the xml documents into actual GUI elements"""

import xml.dom.minidom as minidom
#import widgets


class ParseError(Exception):
    """Raised when an error occurs while parsing an xml document"""
    def __init__(self, msg, filename):
        Exception.__init__(self, msg)
        self.filename = filename

    def __str__(self):
        return self.message + " (filename: %s)" % self.filename


def load_xml(filename):
    """load an xml file and return the resulting widget

    this loads the filename given, turns it into a dom object,
    and then hands it over to the parse function, so that it can create a widget from it.
    the widget is then returned.
    """
    root = minidom.parse(filename).documentElement
    if root.tagName != "gamegoo":
        raise ParseError("'%s' does not seem to be a valid GameGoo XML document (invalid root node)" % filename)
    return parse(root)

def parse(node, parent=None):
    """Parse the DOM and create the widgets from it

    this function takes an xml DOM node and creates a widget from it.
    The node is attached to the parent, if specified. if the node is not attached to any parent.
    the function hands the nodes' children to the created widget to also be parsed.
    """
    widget = get_widget(node)(parent)

def get_widget(node):
    """Retrieve a widget for a certain node.
    
    Every node has an associated widget that must be built. This function fetches
    the relevant class to do so. It uses the string of the tagname to retrieve the right class.
    """
    try:
        return getattr(minidom, node.tagName)
    except AttributeError:
        raise ParseError("encountered invalid tag: '%s'" % node.tagName, node.ownerDocument.documentURI)
 
def get_attributes(node):
    """retrieve a dictionary of the attributes for a node"""
    attr_map = node.attributes
    attributes = (attr_map.item(i) for i in range(attr_map.length))
    return dict((attr.name, attr.value) for attr in attributes)


if __name__ == '__main__':
    example = """<rootnode attr="4" second="3"><firstchild /><secondchild atrr="5" /></rootnode>"""
    parse(minidom.parseString(example).documentElement)
