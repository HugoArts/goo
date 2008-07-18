#! /usr/bin/env python

"""containers - elements that can contain other elements

containers can (obviously) contain other elements, including other containers. Different containers
may draw different borders or backgrounds, and can also arrange their children differently
"""

__all__ = ["base", "sizer"]

from goo.containers.base  import Container, HrContainer
from goo.containers.sizer import Sizer, HrSizer
