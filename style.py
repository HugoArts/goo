#! /usr/bin/env python

import pygame 

"""style.py - The GUI Style object.

the Style object is used to apply different styles to gui elements. The object functions like a dictionary
"""

#this are used in multiple options
DEFAULT_SURFACE = pygame.Surface((100, 100))
DEFAULT_SURFACE.set_colorkey((0, 0, 0))
DEFAULT_TEXTSIZE = 30

# the default style options are picked if no option is set by the user
DEFAULT_STYLE = {
    # button style attributes
    'button_image': DEFAULT_SURFACE,
    'button_focus': DEFAULT_SURFACE,
    'button_click': DEFAULT_SURFACE,
    'button_margin': 10,

    # menu item style attributes
    'menu_item_image': DEFAULT_SURFACE,
    'menu_item_focus': DEFAULT_SURFACE,
    'menu_item_click': DEFAULT_SURFACE,
    'menu_item_margin': 10,
    'menu_margin': 30,

    # slider bar style attributes
    'slider_bar': DEFAULT_SURFACE,
    'slider_cap': DEFAULT_SURFACE,
    'slider_button': DEFAULT_SURFACE,

    # Text style attributes
    'text_font':  pygame.font.Font(None, DEFAULT_TEXTSIZE),
    'text_size':  DEFAULT_TEXTSIZE,
    'text_color': (0,0,0),
}


class Style(dict):
    """Style - an object determining the style of a GUI element"""

    def __init__(self, **kwargs):
        """Create a new Style object.

        Any options that you don't specify will be taken from the default options. The options
        are passed into the constructor as keyword arguments. If you have options in a dictionary, use extended
        call syntax: Style(**options)
        """
        dict.__init__(self)
        for key, val in dic.iteritems():
            if key in DEFAULT_STYLE:
                self[key] = val

    def __setitem__(self, key, value):
        """set a style option.

        The method checks for invalid option names, and verifies the type of the object.
        A KeyError is raised if you try to set a non-existant option. A value of the wrong type causes
        a TypeError.
        """
        if key not in DEFAULT_STYLE:
            raise KeyError("Attempt to set invalid GUI style option: '%s'" % key)
        elif type(value) != type(DEFAULT_STYLE[key]):
            raise TypeError("Attempt to set '%s' to value of the wrong type (was '%s' instead of '%s')" 
                             % (key, type(value), type(DEFAULT_STYLE[key]))
        else:
            dict.__setitem__(self, key, value)

    def __missing__(self, key):
        """called in case a non-existant key is requested

        It might be the case that the item is simply not set in this instance.
        Therefore, we first check if there is a default value for this setting available.
        If that is not the case either, the key is invalid, and we must raise a KeyError
        """
        if key in self.DEFAULT_STYLE:
            return self.DEFAULT_STYLE[key]
        else:
            raise KeyError("Attempt to retrieve invalid GUI style option: '%s'" % key)
