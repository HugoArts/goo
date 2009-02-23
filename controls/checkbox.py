#! /usr/bin/env python

"""implement a checkbox control"""

import base
import goo.draw
import gunge.event
import pygame

class Checkbox(base.Control):
    """A checkbox control that can be flipped on or off"""

    def __init__(self, parent, **attributes):
        self.checked = attributes.get('checked', False)
        self.description = attributes.get('description', None)
        self.icon = goo.img_loader["check.png"]
        self.mouse_over = False
        base.Control.__init__(self, parent, style="default_checkbox", **attributes)

    def create(self):
        self.img = pygame.Surface((12, 12))
        self.img.fill(self.style['background_color'])
        self.rect = self.img.get_rect()
        pygame.draw.rect(self.img, self.style['border_color'], self.rect, self.style['border_width'])

    @gunge.event.bind(pygame.MOUSEBUTTONUP, {'button': 1})
    def on_mouseup(self, event):
        if self.rect.collidepoint(event.pos):
            self.checked = not self.checked

    @gunge.event.bind(gunge.event.UPDATE)
    def update(self, event):
        base.Control.update(self, event)
        self.mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())

    @gunge.event.bind(gunge.event.RENDER)
    def render(self, event):
        surface = event.display.screen
        base.Control.render(self, event)
        if self.checked:
            surface.blit(self.icon, (self.rect.left + self.style['padding'], self.rect.top + self.style['padding']))
