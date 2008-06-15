#! /usr/bin/env python

"""controls.py - leaf elements that the user interacts with such as textboxes or buttons"""

import goo.element


class Control(goo.element.Element):
    """Base class for all controls"""
    #this class might need universal functionality later, but for now its just to
    #differentiate controls from other elements through isinstance/issubclass
    pass


#TODO make create function for the button class
class Button(Control):
    """Class for a button with some text on it that can be clicked"""

    def __init__(self, parent, text, **attributes):
        """Initialize the button"""
        Control.__init__(self, parent, **attributes)
        gunge.event.EventManager.bindToGlobal(
            (pygame.MOUSEBUTTONDOWN, self.on_mousedown, {'button':1}),
            (pygame.MOUSEBUTTONUP,   self.on_mouseup,   {'button':1}))

        self.text = text
        self.mouseover = False
        self.focus = False
        self.down = False

    def on_mousedown(self, event):
        """Check if the mouse is on the button, and click if it is."""
        if not self.hidden and self.rect.collidepoint(event.pos):
            self.down = True

    def on_mouseup(self, event):
        """release the button if the mouse is released, possibly click"""
        if not self.hidden and self.rect.collidepoint(event.pos):
            self.click()
        self.down = False

    def click(self):
        """fire a BUTTONCLICK event with this button and button id if available"""
        event = pygame.event.Event(goo.BUTTONCLICK, {'button': self, 'objectid': self.id})
        pygame.event.post(event)
