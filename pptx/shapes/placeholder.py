# encoding: utf-8

"""
Placeholder object, a wrapper (decorator pattern) around an autoshape having
a ``ph`` element. Provides access to placeholder-specific properties of the
shape, such as the placeholder type. All other attribute gets are forwarded
to the underlying shape.
"""

from pptx.oxml.ns import namespaces
from pptx.shapes.autoshape import Shape
from pptx.spec import PH_ORIENT_HORZ, PH_SZ_FULL, PH_TYPE_OBJ


# default namespace map for use in lxml calls
_nsmap = namespaces('a', 'r', 'p')


class Placeholder(object):
    """
    Decorator (pattern) class for adding placeholder properties to a shape
    that contains a placeholder element, e.g. ``<p:ph>``.
    """
    def __new__(cls, shape):
        cls = type('PlaceholderDecorator', (Placeholder, shape.__class__), {})
        return object.__new__(cls)

    def __init__(self, shape):
        self._decorated = shape
        xpath = './*[1]/p:nvPr/p:ph'
        self._ph = self._element.xpath(xpath, namespaces=_nsmap)[0]

    def __getattr__(self, name):
        """
        Called when *name* is not found in *self* (attribute) or in class
        tree (methods). In this case, attribute lookup is delegated to
        underlying shape.
        """
        return getattr(self._decorated, name)

    @property
    def type(self):
        """
        Placeholder type, e.g. PH_TYPE_CTRTITLE
        """
        return self._ph.get('type', PH_TYPE_OBJ)

    @property
    def orient(self):
        """
        Placeholder 'orient' attribute, e.g. PH_ORIENT_HORZ
        """
        return self._ph.get('orient', PH_ORIENT_HORZ)

    @property
    def sz(self):
        """
        Placeholder 'sz' attribute, e.g. PH_SZ_FULL
        """
        return self._ph.get('sz', PH_SZ_FULL)

    @property
    def idx(self):
        """
        Placeholder 'idx' attribute, e.g. '0'
        """
        return int(self._ph.get('idx', 0))


class BasePlaceholder(Shape):
    """
    Base class for placeholder subclasses that differentiate the varying
    behaviors of placeholders on a master, layout, and slide.
    """
