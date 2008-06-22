#! /usr/bin/env python

"""controls.py - leaf elements that the user interacts with such as textboxes or buttons"""

import gunge
import goo.element, goo.draw
import pygame


class Control(goo.element.Element):
    """Base class for all controls"""
    
    def __init__(self, parent, **attributes):
        """initialize the control
        
        all this currently does is create the element.
        """
        goo.element.Element.__init__(self, parent, **attributes)
        self.create()


#TODO make create function for the button class
class Button(Control):
    """Class for a button with some text on it that can be clicked"""

    def __init__(self, parent, text, **attributes):
        """Initialize the button"""
        gunge.event.EventManager.bindToGlobal(
            (pygame.MOUSEBUTTONDOWN, self.on_mousedown, {'button':1}),
            (pygame.MOUSEBUTTONUP,   self.on_mouseup,   {'button':1}))

        self.text = text
        Control.__init__(self, parent, **attributes)

        self.mouseover = False
        self.focus = False
        self.down = False

    def create(self):
        """creates the button"""
        font = pygame.font.Font(self.style['font'], self.style['font_height'])
        txtimg = font.render(self.text, True, self.style['font_color'])
        txtrect = txtimg.get_rect()

        self.rect = pygame.Rect(0, 0, txtrect.width + self.style['margin'], txtrect.height + self.style['margin'])
        txtrect.center = self.rect.center
        self.img = goo.draw.alpha_surface(self.rect.size)
        goo.draw.rounded_rect(self.img, self.rect, self.style)
        self.img.blit(txtimg, txtrect)

        self.parent.adjust(self)

    def on_mousedown(self, event):
        """Check if the mouse is on the button, and click if it is."""
        if not self.hidden and self.rect.collidepoint(event.pos):
            self.down = True

    def on_mouseup(self, event):
        """release the button if the mouse is released, possibly click"""
        if self.down and not self.hidden and self.rect.collidepoint(event.pos):
            self.click()
        self.down = False

    def click(self):
        """fire a BUTTONCLICK event with this button and button id if available"""
        event = pygame.event.Event(goo.BUTTONCLICK, {'button': self, 'objectid': self.id})
        pygame.event.post(event)
