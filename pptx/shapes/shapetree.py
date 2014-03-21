# encoding: utf-8

"""
The shape tree, the structure that holds a slide's shapes.
"""

from pptx.oxml.autoshape import CT_Shape
from pptx.oxml.graphfrm import CT_GraphicalObjectFrame
from pptx.oxml.ns import _nsmap, qn
from pptx.oxml.picture import CT_Picture
from pptx.shapes.autoshape import AutoShapeType, Shape
from pptx.shapes.picture import Picture
from pptx.shapes.placeholder import Placeholder
from pptx.shapes.shape import BaseShape
from pptx.shapes.table import Table
from pptx.spec import slide_ph_basenames
from pptx.spec import PH_ORIENT_VERT, PH_TYPE_DT, PH_TYPE_FTR, PH_TYPE_SLDNUM


def BaseShapeFactory(shape_elm, parent):
    """
    Return an instance of the appropriate shape proxy class for *shape_elm*.
    """
    tag_name = shape_elm.tag
    if tag_name == qn('p:sp'):
        return Shape(shape_elm, parent)
    if tag_name == qn('p:pic'):
        return Picture(shape_elm, parent)
    if tag_name == qn('p:graphicFrame'):
        if shape_elm.has_table:
            return Table(shape_elm, parent)
    return BaseShape(shape_elm, parent)


class BaseShapeTree(object):
    """
    Base class for a shape collection appearing in a slide-type object,
    include Slide, SlideLayout, and SlideMaster, providing common methods.
    """
    def __init__(self, slide):
        super(BaseShapeTree, self).__init__()
        self._slide = slide

    def __getitem__(self, idx):
        """
        Return shape at *idx* in sequence, e.g. ``shapes[2]``.
        """
        shape_elms = list(self._iter_shape_elms())
        try:
            shape_elm = shape_elms[idx]
        except IndexError:
            raise IndexError('shape index out of range')
        return self._shape_factory(shape_elm)

    def __iter__(self):
        """
        Generate a reference to each shape in the collection, in sequence.
        """
        for shape_elm in self._iter_shape_elms():
            yield self._shape_factory(shape_elm)

    def __len__(self):
        """
        Return count of shapes in this shape tree. A group shape contributes
        1 to the total, without regard to the number of shapes contained in
        the group.
        """
        shape_elms = list(self._iter_shape_elms())
        return len(shape_elms)

    def _iter_shape_elms(self):
        """
        Generate each child of the ``<p:spTree>`` element that corresponds to
        a shape, in the sequence they appear in the XML.
        """
        shape_tags = (
            qn('p:sp'), qn('p:grpSp'), qn('p:graphicFrame'), qn('p:cxnSp'),
            qn('p:pic'), qn('p:contentPart')
        )
        spTree = self._slide.spTree
        for elm in spTree.iterchildren():
            if elm.tag in shape_tags:
                yield elm

    def _shape_factory(self, shape_elm):
        """
        Return an instance of the appropriate shape proxy class for
        *shape_elm*.
        """
        return BaseShapeFactory(shape_elm, self)


class ShapeCollection(BaseShape):
    """
    The sequence of shapes that appears on a slide. The first shape in the
    sequence is the backmost in z-order and the last shape is topmost.
    Supports indexed access, len(), index(), and iteration.
    """
    _NVGRPSPPR = qn('p:nvGrpSpPr')
    _GRPSPPR = qn('p:grpSpPr')
    _SP = qn('p:sp')
    _GRPSP = qn('p:grpSp')
    _GRAPHICFRAME = qn('p:graphicFrame')
    _CXNSP = qn('p:cxnSp')
    _PIC = qn('p:pic')
    _CONTENTPART = qn('p:contentPart')
    _EXTLST = qn('p:extLst')

    def __init__(self, spTree, slide=None):
        super(ShapeCollection, self).__init__(spTree, slide)
        self._spTree = spTree
        self._slide = slide
        self._shapes = []
        # unmarshal shapes
        for elm in spTree.iterchildren():
            if elm.tag in (self._NVGRPSPPR, self._GRPSPPR, self._EXTLST):
                continue
            elif elm.tag == self._SP:
                shape = Shape(elm, self)
            elif elm.tag == self._PIC:
                shape = Picture(elm, self)
            # elif elm.tag == self._GRPSP:
            #     shape = ShapeCollection(elm)
            elif elm.tag == self._GRAPHICFRAME:
                if elm.has_table:
                    shape = Table(elm, self)
                else:
                    shape = BaseShape(elm, self)
            # elif elm.tag == self._CONTENTPART:
            #     msg = ("first time 'contentPart' shape encountered in the "
            #            "wild, please let developer know and send example")
            #     raise ValueError(msg)
            else:
                shape = BaseShape(elm, self)
            self._shapes.append(shape)

    def __getitem__(self, idx):
        return self._shapes.__getitem__(idx)

    def __iter__(self):
        return self._shapes.__iter__()

    def __len__(self):
        return self._shapes.__len__()

    def add_picture(self, img_file, left, top, width=None, height=None):
        """
        Add picture shape displaying image in *img_file*, where *img_file*
        can be either a path to a file (a string) or a file-like object.
        """
        image, rId = self._slide._add_image(img_file)

        id = self._next_shape_id
        name = 'Picture %d' % (id-1)
        desc = image._desc
        width, height = image._scale(width, height)

        pic = CT_Picture.new_pic(id, name, desc, rId, left, top, width, height)

        self._spTree.append(pic)
        picture = Picture(pic, self)
        self._shapes.append(picture)
        return picture

    def add_shape(self, autoshape_type_id, left, top, width, height):
        """
        Add auto shape of type specified by *autoshape_type_id* (like
        ``MSO.SHAPE_RECTANGLE``) and of specified size at specified position.
        """
        autoshape_type = AutoShapeType(autoshape_type_id)
        id_ = self._next_shape_id
        name = '%s %d' % (autoshape_type.basename, id_-1)

        sp = CT_Shape.new_autoshape_sp(id_, name, autoshape_type.prst,
                                       left, top, width, height)
        shape = Shape(sp, self)

        self._spTree.append(sp)
        self._shapes.append(shape)
        return shape

    def add_table(self, rows, cols, left, top, width, height):
        """
        Add table shape with the specified number of *rows* and *cols* at the
        specified position with the specified size. *width* is evenly
        distributed between the *cols* columns of the new table. Likewise,
        *height* is evenly distributed between the *rows* rows created.
        """
        id = self._next_shape_id
        name = 'Table %d' % (id-1)
        graphicFrame = CT_GraphicalObjectFrame.new_table(
            id, name, rows, cols, left, top, width, height)
        self._spTree.append(graphicFrame)
        table = Table(graphicFrame, self)
        self._shapes.append(table)
        return table

    def add_textbox(self, left, top, width, height):
        """
        Add text box shape of specified size at specified position.
        """
        id_ = self._next_shape_id
        name = 'TextBox %d' % (id_-1)

        sp = CT_Shape.new_textbox_sp(id_, name, left, top, width, height)
        shape = Shape(sp, self)

        self._spTree.append(sp)
        self._shapes.append(shape)
        return shape

    def index(self, item):
        """
        Return the index of *shape* in this sequence, raising |ValueError| if
        *shape* is not in the collection.
        """
        return self._shapes.index(item)

    @property
    def placeholders(self):
        """
        Immutable sequence containing the placeholder shapes in this shape
        collection, sorted in *idx* order.
        """
        placeholders = (
            [Placeholder(sp) for sp in self._shapes if sp.is_placeholder]
        )
        placeholders.sort(key=lambda ph: ph.idx)
        return tuple(placeholders)

    @property
    def title(self):
        """The title shape in collection or None if no title placeholder."""
        for shape in self._shapes:
            if shape._is_title:
                return shape
        return None

    def _clone_layout_placeholders(self, slidelayout):
        """
        Add placeholder shapes based on those in *slidelayout*. Z-order of
        placeholders is preserved. Latent placeholders (date, slide number,
        and footer) are not cloned.
        """
        latent_ph_types = (PH_TYPE_DT, PH_TYPE_SLDNUM, PH_TYPE_FTR)
        for sp in slidelayout.shapes:
            if not sp.is_placeholder:
                continue
            ph = Placeholder(sp)
            if ph.type in latent_ph_types:
                continue
            self._clone_layout_placeholder(ph)

    def _clone_layout_placeholder(self, layout_ph):
        """
        Add a new placeholder shape based on the slide layout placeholder
        *layout_ph*.
        """
        id_ = self._next_shape_id
        ph_type = layout_ph.type
        orient = layout_ph.orient
        shapename = self._next_ph_name(ph_type, id_, orient)
        sz = layout_ph.sz
        idx = layout_ph.idx

        sp = CT_Shape.new_placeholder_sp(id_, shapename, ph_type, orient,
                                         sz, idx)
        shape = Shape(sp, self)

        self._spTree.append(sp)
        self._shapes.append(shape)
        return shape

    def _next_ph_name(self, ph_type, id, orient):
        """
        Next unique placeholder name for placeholder shape of type *ph_type*,
        with id number *id* and orientation *orient*. Usually will be standard
        placeholder root name suffixed with id-1, e.g.
        _next_ph_name(PH_TYPE_TBL, 4, 'horz') ==> 'Table Placeholder 3'. The
        number is incremented as necessary to make the name unique within the
        collection. If *orient* is ``'vert'``, the placeholder name is
        prefixed with ``'Vertical '``.
        """
        basename = slide_ph_basenames[ph_type]
        # prefix rootname with 'Vertical ' if orient is 'vert'
        if orient == PH_ORIENT_VERT:
            basename = 'Vertical %s' % basename
        # increment numpart as necessary to make name unique
        numpart = id - 1
        names = self._spTree.xpath('//p:cNvPr/@name', namespaces=_nsmap)
        while True:
            name = '%s %d' % (basename, numpart)
            if name not in names:
                break
            numpart += 1
        return name

    @property
    def _next_shape_id(self):
        """
        Next available drawing object id number in collection, starting from 1
        and making use of any gaps in numbering. In practice, the minimum id
        is 2 because the spTree element is always assigned id="1".
        """
        cNvPrs = self._spTree.xpath('//p:cNvPr', namespaces=_nsmap)
        ids = [int(cNvPr.get('id')) for cNvPr in cNvPrs]
        ids.sort()
        # first gap in sequence wins, or falls off the end as max(ids)+1
        next_id = 1
        for id in ids:
            if id > next_id:
                break
            next_id += 1
        return next_id
