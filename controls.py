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
        self.img = goo.draw.alpha_surface(self.rect.size)
        goo.draw.rounded_rect(self.img, self.rect, self.style)

        self.txtimg = txtimg
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

    def update(self):
        """update the button"""
        Control.update(self)
        self.mouseover = self.rect.collidepoint(pygame.mouse.get_pos())
        self.down = self.down and self.mouseover

    def render(self, surface):
        """render the button"""
        txtrect = self.txtimg.get_rect()
        txtrect.center = self.rect.center
        if self.down:
            goo.draw.rounded_rect(surface, self.rect, (self.style['button_down'], 0, self.style['border_radius']))
            txtrect.move_ip(0, 1)
        elif self.mouseover:
            goo.draw.rounded_rect(surface, self.rect, (self.style['button_hover'], 0, self.style['border_radius']))

        Control.render(self, surface)
        surface.blit(self.txtimg, txtrect)

        if self.mouseover:
            style = [self.style['border_hover'], self.style['border_width'], self.style['border_radius']+2]
            goo.draw.rounded_rect(surface, self.rect.inflate(2*style[1], 2*style[1]), style)
