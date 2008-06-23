#! /usr/bin/env python

"""parser.py: parse the xml documents into actual GUI elements"""

import xml.dom.minidom as minidom
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
    doc = minidom.parse(filename)
    root = doc.documentElement
    if root.tagName != "gamegoo":
        raise ParseError("Invalid GameGoo XML document: invalid root node", filename)

    if ids is None:
        node = root.firstChild
        while node.nodeType == 3:
            node = node.nextSibling
        widget = parse(node)
        widget.arrange()
        return widget
    elif ids is PARSE_ALL:
        widgets = tuple(parse(node) for node in root.childNodes if node.nodeType != 3)
    else:
        widgets = tuple(parse(doc.getElementById(i)) for i in ids)

    #these widgets will have no parent, and must be arranged
    for widget in widgets:
        widget.arrange()
    return widgets

def parse(node, parent=None):
    """Parse the DOM and create the widgets from it

    takes an xml DOM node and creates a widget from it.
    The node is attached to the parent, if specified. Otherwise, the special NullParent is used.
    the nodes' children are handed to the created widget to also be parsed.
    """
    if parent is None:
        parent = goo.NullParent()

    if node.hasChildNodes():
        widget = get_widget(node)(parent, node.childNodes, **get_attributes(node))
    else:
        widget = get_widget(node)(parent, **get_attributes(node))
    gunge.mv.ModelView.get_global().add(widget)
    return widget

def get_widget(node):
    """Retrieve a widget for a certain node.
    
    Every node has an associated widget that must be built. This function fetches
    the relevant class to do so. It uses the string of the tagname to retrieve the right class.
    """
    #the widget could be located in one of several modules. We'll have to try them all
    for module in (goo.controls, goo.containers):
        try:
            return getattr(module, node.tagName)
        except AttributeError:
            continue
    raise ParseError("encountered invalid tag: '%s'" % node.tagName, node.ownerDocument.documentURI)
 
def get_attributes(node):
    """retrieve a dictionary of the attributes for a node"""
    attr_map = node.attributes
    attributes = (attr_map.item(i) for i in range(attr_map.length))
    return dict((str(attr.name), attr.value) for attr in attributes)


if __name__ == '__main__':
    example = """<rootnode attr="4" second="3"><firstchild /><secondchild atrr="5" /></rootnode>"""
    parse(minidom.parseString(example).documentElement)
