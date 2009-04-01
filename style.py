#! /usr/bin/env python

import pygame

"""style.py - The GUI Style object.

the Style object is used to apply different styles to gui elements.
The object functions like a dictionary
"""
# this is used in multiple options
DEFAULT_SURFACE = pygame.Surface((100, 100))
DEFAULT_SURFACE.set_colorkey((0, 0, 0))

#TODO: change the default options to correct ones
# the DEFAULT_OPTIONS style options are picked if no option is set by the user
DEFAULT_OPTIONS = {
    'margin': 10,
    'padding': 12,

    'background_color': (236, 233, 233),
    'hover_color':      (225, 230, 240),
    'clicked_color':    (200, 200, 200),

    'border_color': (193, 186, 186),
    'border_hover': (20, 100, 145),
    'border_width': 1,
    'border_radius': 5,
    'border_rounding': 0xF,

    'font': "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    'font_height': 12,
    'font_color':  (0, 0, 0),
}


class Style(dict):
    """Style - an object determining the style of a GUI element

    passed into almost any element to determine its style. You can initialize
    this without passing in anything to use the DEFAULT_OPTIONS style. Note that
    when iterating, printing, or calling methods such as iteritems() on
    this object, options not set (i.e. defaults) are not included.
    """
    __slots__ = 'name'

    def __init__(self, name, **kwargs):
        """Create a new Style object.

        Any options that you don't specify will be taken from the DEFAULT_OPTIONS
        options. The options are passed into the constructor as keyword
        arguments. If you have options in a dictionary, use extended call
        syntax: Style(**options)
        """
        dict.__init__(self)
        for key, value in kwargs.items():
            self[key] = value
        self.name = name

    def __setitem__(self, key, value):
        """set a style option.

        The method checks for invalid option names, and verifies the type of
        the object. A KeyError is raised if you try to set a non-existant
        option. A value of the wrong type causes a TypeError.
        """
        if key not in DEFAULT_OPTIONS:
            raise KeyError("Attempt to set invalid GUI style option: '%s'" % key)
        elif type(value) != type(DEFAULT_OPTIONS[key]):
            raise TypeError("new value of '%s' is of wrong type ('%s' instead of '%s')" % (key, type(value), type(DEFAULT_OPTIONS[key])))
        else:
            dict.__setitem__(self, key, value)

    def __missing__(self, key):
        """called in case a non-existant key is requested

        It might be the case that the item is simply not set in this instance.
        Therefore, we first check if there is a DEFAULT_OPTIONS value for this setting
        available. If that is not the case either, the key is invalid, and we
        must raise a KeyError.
        """
        if key in DEFAULT_OPTIONS:
            return DEFAULT_OPTIONS[key]
        else:
            raise KeyError("Attempt to retrieve invalid GUI style option: '%s'" % key)

    def __str__(self):
        return "<Style %s %s>" % (self.name, dict.__str__(self)) 

    def font(self):
        """shortcut for making a font object from this goo style object"""
        return pygame.font.Font(self['font'], self['font_height'])


# dict of all registered styles. Styles must be registered to be recognised in XML
style_dict = {'default': Style("default")}

def add(style):
    """add a style to the XML-recognised style list

    note that if a style with the same name was already present, it will be overwritten.
    """
    style_dict[style.name] = style

def get(name='default'):
    """retrieve a style from the XML-recognised style list by its name"""
    return style_dict[name]

def align(element, area, arg):
    """align the element in the given area

    the argument can be either 'left', 'right', or 'center'
    """
    if arg == "left":
        element.pos = area.left, element.pos[1]
    elif arg == "right":
        element.pos = area.right - element.rect.width, element.pos[1]
    elif arg == "center":
        element.pos = area.centerx - (element.rect.width / 2), element.pos[1]
    else:
        raise RuntimeError("Invalid value of attribute align: %s" % arg)

def valign(element, area, arg):
    """align the element vertically in the given area

    same as align, but vertical. The argument can be one of: 'top', 'bottom', 'center'
    """
    if arg == "top":
        element.pos = element.pos[0], area.top
    elif arg == "bottom":
        element.pos = element.pos[0], area.bottom - element.rect.height
    elif arg == "center":
        element.pos = element.pos[0], area.centery - (element.rect.height / 2)
    else:
        raise RuntimeError("Invalid value of attribute valign: %s" % arg)

def expand(element, area, arg):
    """expand the element to cover all available space

    argument can be either True or False. Of course, the false case is default,
    so rather pointless, but it's there for the sake of consistency
    """
    if arg == "True":
        element.pos = area.topleft
        element.rect.size = area.size
        #we've changed our size! better rearrange children
        element.arrange_children()
    elif arg != "False":
        raise RuntimeError("Invalid value of attribute expand: %s" % arg)
