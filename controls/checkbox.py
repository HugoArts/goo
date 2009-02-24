#! /usr/bin/env python

"""implement a checkbox control"""

import base
import goo.draw
import gunge.event
import pygame

class Checkbox(base.Control):
    """A checkbox control that can be flipped on or off"""

    def __init__(self, parent, **attributes):
        """initialize Checkbox instance"""
        self.checked = attributes.get('checked', False) == "True"
        self.description = attributes.get('description', "")
        self.icon = goo.img_loader["check.png"]
        self.mouse_over = False
        base.Control.__init__(self, parent, style="default_checkbox", **attributes)

    def create(self):
        """create the checkbox surface"""
        font = pygame.font.Font(self.style['font'], self.style['font_height'])
        txtimg = font.render(self.description, True, self.style['font_color'])
        txtrect = txtimg.get_rect()

        self.img = goo.draw.alpha_surface((16 + txtrect.width +  + 2*self.style['padding'], max(12, txtrect.height) + 2*self.style['padding']))
        self.rect = self.img.get_rect()
        self.box_rect = pygame.Rect((self.style['padding'],)*2, (12, 12))
        self.box_rect.centery = self.rect.height / 2.

        self.img.fill(self.style['background_color'], self.box_rect)
        self.img.blit(txtimg, (16, self.style['padding']))

        pygame.draw.rect(self.img, self.style['border_color'], self.box_rect, self.style['border_width'])
        self.parent.adjust(self)

    @gunge.event.bind(pygame.MOUSEBUTTONUP, {'button': 1})
    def on_mouseup(self, event):
        """if the MOUSEUP collides with the checkbox, change the checked attribute and send out a CHECKCHANGED event"""
        if self.rect.collidepoint(event.pos):
            self.checked = not self.checked
            event = pygame.event.Event(goo.CHECKCHANGED, {'objectid': self.id, 'objecttype': type(self), 'checked': self.checked})
            pygame.event.post(event)

    @gunge.event.bind(gunge.event.UPDATE)
    def update(self, event):
        """update the checkbox. Bound to gunge.event.UPDATE"""
        base.Control.update(self, event)
        self.mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())

        self.box_rect.topleft = self.rect.topleft
        self.box_rect.left += self.style['padding']
        self.box_rect.centery = self.rect.centery

    @gunge.event.bind(gunge.event.RENDER)
    def render(self, event):
        """render the checkbox. Bound to gunge.event.RENDER"""
        surface = event.display.screen
        if self.mouse_over:
            pygame.draw.rect(surface, self.style['hover_color'], self.rect, 0)
        base.Control.render(self, event)

        if self.checked:
            surface.blit(self.icon, (self.box_rect.left + 1, self.box_rect.top + 1))
