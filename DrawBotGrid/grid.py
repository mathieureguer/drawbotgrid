import drawBot as db
import math

# ----------------------------------------

"""
Weirdly enough, baselineShift behavior seems to have changed in macOs 10.15 and 11.xx. 
And reverted backt ot the old behavior in 12.xx 
"""
import platform
plat = platform.mac_ver()[0]

if plat.startswith(("10.15", "11")):
    BASELINE_SHIFT_RATIO_ADJUST = 1
else:
    BASELINE_SHIFT_RATIO_ADJUST = .5

# ----------------------------------------


class PseudoInt():
    def __init__(self, value):
        self.value = value

    def __index__(self):
        return self.value

    def __index__(self):
        return (db.height() - self.value)

    def __add__(self, other):
        return other + self.__index__()

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return - other + self.__index__()

    def __rsub__(self, other):
        return self.__sub__(other)

    def __repr__(self):
        return(f"<{self.__class__.__name__} {self.value} -> {self.__index__()}>")


class TopCoord(PseudoInt):
    def __index__(self):
        return db.height() - self.value


class ReverseTopCoord(PseudoInt):
    def __index__(self):
        return self.value - db.height()


class Columns():
    def __init__(self, columns, gutter, margins_left_top_right_bottom):
        self.columns = columns
        self.gutter = gutter
        self.margin_left, self.margin_top, self.margin_right, self.margin_bottom = margins_left_top_right_bottom

    @property
    def width(self):
        return (db.width() - self.margin_left + self.margin_right - (self.columns - 1) * self.gutter) / self.columns

    @property
    def height(self):
        return db.height() - self.margin_bottom + self.margin_top

    def span(self, span):
        return self.width * span + self.gutter * (span - 1)

    def __getitem__(self, index):
        # assert index <= self.columns
        return self.margin_left + index * (self.gutter + self.width)

    def __len__(self):
        return self.columns

    def __iter__(self):
        return iter([self.__getitem__(i) for i in range(self.columns)])

    def draw(self):
        for c in self:
            db.rect(c, self.margin_bottom, self.width, self.height)


class BaselineGrid():
    def __init__(self, line_height, margin_top=0, margin_bottom=0):
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.line_height = line_height

    def __getitem__(self, index):
        # assert index <= self.columns
        # return self.values[index]
        if index > 0:
            return db.height() - self.margin_top - index * self.line_height
        else:
            return self.values[index]

    def __len__(self):
        height = db.height() + self.margin_top - self.margin_bottom
        return height // self.line_height + 1

    def __iter__(self):
        return iter(self.values)

    @property
    def values(self):
        return [db.height() - self.margin_top - index * self.line_height for index in range(len(self))]

    def span(self, span):
        return self.line_height * span

    def draw(self):
        for c in self:
            db.line((0, c), (db.width(), c))

    def baseline_index_from_coordinate(self, y):
        """
        Return the line index for the baseline right below the coordinate
        """
        for i, v in enumerate(self.values):
            if v < y:
                return i
        return None


# ----------------------------------------

def draw_image_at_size(path, possize, preserve_proprotions=True):
    x, y, w, h = possize
    actual_w, actual_h = db.imageSize(path)
    if not w:
        scale_ratio_w = h / actual_h
        scale_ratio_h = h / actual_h
    elif not h:
        scale_ratio_w = w / actual_w
        scale_ratio_h = w / actual_w
    else:
        scale_ratio_w = w / actual_w
        scale_ratio_h = h / actual_h

        if preserve_proprotions:
            scale_ratio = min(scale_ratio_w, scale_ratio_h)
            scale_ratio_w = scale_ratio
            scale_ratio_h = scale_ratio

    with db.savedState():
        db.translate(x, y)
        db.scale(scale_ratio_w, scale_ratio_h)
        db.image(path, (0, 0))

# ----------------------------------------


def grid_text_box(txt, box, grid, align_first_line_only=False, align=None):
    with db.savedState():
        # textBloc does not like negative height
        box = correct_box_direction(box)

        x, y, w, h = box
        if not align_first_line_only:
            actual_line_height = db.fontLineHeight()
            target_line_height = math.ceil(actual_line_height / grid) * grid
            db.lineHeight(target_line_height)

        # calculate first line offset
        font_top = db.fontCapHeight()
        target_first_line = math.ceil(font_top / grid) * grid
        actual_first_line = get_first_line_height_relative_to_box(txt, (x, y, w, h))
        offset = actual_first_line - target_first_line
        db.baselineShift(offset * BASELINE_SHIFT_RATIO_ADJUST)

        db.textBox(txt, (x, y, w, h), align=align)


def get_first_line_height_relative_to_box(txt, box):
    x, y, w, h = box
    absolute_first_line_x, absolute_first_line_y = db.textBoxBaselines(txt, box)[0]
    relative_first_line_y = y + h - absolute_first_line_y
    return relative_first_line_y


def correct_box_direction(box):
    x, y, w, h = box
    if h < 0:
        y = y + h
        h = h * -1
    return(x, y, w, h)

# ----------------------------------------


def vertically_centered_text_box(text, box, align=None):
    with db.savedState():
        text = text.strip()
        x, y, w, h = correct_box_direction(box)
        font_top = db.fontCapHeight()
        lines = db.textBoxBaselines(text, (0, 0, w, h))
        top = lines[0][1] + font_top
        # current version will only center the first line
        # bottom = lines[-1][1]
        bottom = lines[0][1]
        text_h = top - bottom
        margin = (h - text_h) / 2
        shift = margin - bottom
        db.baselineShift(shift * BASELINE_SHIFT_RATIO_ADJUST)
        db.textBox(text, (x, y, w, h), align=align)
