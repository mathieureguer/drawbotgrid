import drawBot as db
import math

# ----------------------------------------

class AbstractArea():
    """
    this is mostly a possize, margin manager
    """
    def __init__(self, possize):
        self._x, self._y, self._width, self._height = possize
        
    @classmethod
    def from_margins(cls, margins, *args):
        left_margin, bottom_margin, right_margin, top_margin = margins
        possize = (-left_margin, -bottom_margin, db.width()+ left_margin + right_margin, db.height() + bottom_margin + top_margin)
        return cls(possize, *args)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def top(self):
        """
        the absolute y value of the top of the grid
        """
        return self._y + self._height

    @property
    def bottom(self):
        """
        the absolute y value of the bottom of the grid
        """
        return self.y

    @property
    def left(self):
        """
        the absolute x value of the left of the grid
        """
        return self.x

    @property
    def right(self):
        """
        the absolute x value of the right of the grid
        """
        return self.x + self.width
   
    # ----------------------------------------
    
    draw_color = (1, 0, 1, 1)
    
    def draw(self, show_index=False):
        with db.savedState():
            db.stroke(*self.draw_color)
            db.fill(None)
            db.strokeWidth(.5)
            self.draw_frame()
            
        if show_index:
            with db.savedState():
                db.stroke(None)
                db.fill(*self.draw_color)
                db.fontSize(5)
                self.draw_indexes()

    def draw_frame(self):
        raise NotImplementedError

    def draw_indexes(self):
        raise NotImplementedError

# ----------------------------------------

class AbstractGutterGrid(AbstractArea):
    """
    this is meant to be subclassed by Columns and Grid
    """
    
    def __init__(self, possize, subdivisions, gutter):
        super().__init__(possize)
        self.subdivisions = subdivisions
        self.gutter = gutter

    # ----------------------------------------

    @property
    def _start_point(self):
        raise NotImplementedError

    @property
    def _end_point(self):
        raise NotImplementedError
           
    # ----------------------------------------

    @property
    def _reference_dimension(self):
        return self._end_point - self._start_point
    
    @property
    def subdivision_dimension(self):
        """
        the absolute dimension of a single subdivision within the grid
        """
        return (self._reference_dimension - ((self.subdivisions - 1) * self.gutter)) / self.subdivisions

    def span(self, span):
        """
        the absolute dimension of a span of consecutive subdivisions within the grid, 
        including their inbetween gutters
        """
        if span >= 0:
            return self.subdivision_dimension * span + self.gutter * (span - 1)
        else:
            return self.subdivision_dimension * span + self.gutter * (span + 1)
    
    # ----------------------------------------
    
    def __getitem__(self, index):
        if index >= 0:
            return self._start_point + index * (self.gutter + self.subdivision_dimension)
        else:
            return self._end_point + (index+1) * (self.gutter + self.subdivision_dimension)

    def __len__(self):
        return self.subdivisions

    def __iter__(self):
        return iter([self.__getitem__(i) for i in range(self.subdivisions)])

    
# ----------------------------------------

class ColumnGrid(AbstractGutterGrid):
    """
    Will return coordinates according to a column based grid.

    Columns are refered to by index, accessing a column index will return its absolute x coordinate in the page.
    
    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    print(my_columns[3])
    > 505.0    
    ```

    Negative indexes refer the right part of a column, starting from the right of the page.
    
    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    print(my_columns[-2])
    > 798.33  
    ```

    The grid can return the total width of a span of consecutive columns, including the related inbween gutters
    
    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    print(my_columns.span(4))
    > 596.66 
    ```

    The whole point is to use this as coordinate helpers to draw shapes of course
    
    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    fill(0, 1, 0, .5)
    rect(my_columns[1], my_columns.bottom, my_columns.span(3), my_columns.height)
    fill(1, 0, 0, .5) 
    rect(my_columns[0], my_columns.top, my_columns.span(3), -200)
    rect(my_columns[2], my_columns.top-200, my_columns.span(1), -200)
    rect(my_columns[5], my_columns.top-400, my_columns.span(2), -200)
    ```
    
    The columns grid can also draw itself, if necessary
    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    fill(None)
    stroke(1, 0, 1)
    strokeWidth(1)
    my_columns.draw()
    ```

    """

    @property
    def columns(self):
        return self.subdivisions

    @property
    def column_width(self):
        return self.subdivision_dimension

    # @property
    # def _reference_dimension(self):
    #     return self.width

    @property
    def _start_point(self):
        return self.left

    @property
    def _end_point(self):
        return self.right

    # ----------------------------------------

    def draw_frame(self):
        for col in self:
            db.rect(col, self.bottom, self.column_width, self.height)

    def draw_indexes(self):
        for i, col in enumerate(self):
            db.text(str(i), (col+2, self.bottom+2))

# ----------------------------------------

class RowGrid(AbstractGutterGrid):
    """
    To be documented :)
    """

    @property
    def rows(self):
        return self.subdivisions

    @property
    def row_height(self):
        return self.subdivision_dimension

    # @property
    # def _reference_dimension(self):
    #     return self.height

    @property
    def _start_point(self):
        return self.bottom

    @property
    def _end_point(self):
        return self.top


    # ----------------------------------------

    def draw_frame(self):
        for row in self:
            db.rect(self.left, row, self.width, self.row_height)

    def draw_indexes(self):
        for i, row in enumerate(self):
            db.text(str(i), (self.left + 2, row+2))


# ----------------------------------------

class Grid(AbstractGutterGrid):
    """
    this is meant to be subclassed by Columns and Grid
    """

    def __init__(self, possize, columns, rows, gutter_columns, gutter_rows):
        self._x, self._y, self._width, self._height = possize
        self.columns = ColumnGrid(possize, columns, gutter_columns)
        self.rows = RowGrid(possize, rows, gutter_rows)


    # ----------------------------------------

    @property
    def _reference_dimension(self):
        return self.width, self.height

    @property
    def _start_point(self):
        return self.left, self.bottom

    @property
    def _end_point(self):
        return self.right, self.top

    # ----------------------------------------
    @property
    def column_width(self):
        return self.columns.column_width

    @property
    def row_height(self):
        return self.rows.row_height

    @property
    def subdivision_dimension(self):
        """
        the absolute dimension of a single subdivision within the grid
        """
        return self.column_width, self.row_height

    def column_span(self, span):
        return self.columns.span(span)

    def row_span(self, span):
        return self.rows.span(span)

    def span(self, column_span, row_span):
        """
        the absolute dimension of a span of consecutive subdivision within the grid, including their inbetween gutters
        """
        return self.column_span(column_span), self.row_span(row_span)
    
    # ----------------------------------------
    
    def __getitem__(self, index):
        assert len(index) == 2
        return self.columns[index[0]], self.rows[index[1]]

    def __len__(self):
        return len(self.columns) * len(self.rows)

    def __iter__(self):
        return iter([(c, r) for c in self.columns for r in self.rows])

    # ----------------------------------------
    
    def draw_frame(self):
        for col, row in self:
            db.rect(col, row, self.column_width, self.row_height)

    def draw_indexes(self):
        # for index_col, col in enumerate(self.columns):
        #     for index_row, row in enumerate(self.rows):
        #         db.text(f"({index_col}, {index_row})", (col+2, row+2))
        self.columns.draw_indexes()
        self.rows.draw_indexes()


# ----------------------------------------


class BaselineGrid(AbstractArea):
    """
    
    """
    
    def __init__(self, possize, line_height):
        self.input_possize = possize
        super().__init__(possize)
        self.line_height = line_height


    # ----------------------------------------

    @property
    def _start_point(self):
        return self.top

    @property
    def _end_point(self):
        return self.y

    @property
    def bottom(self):
        """
        the absolute y value of the bottom of the grid
        """
        # bottom matches the last visible line, it may not be equal self.y
        return self[-1]

    @property
    def height(self):
        """
        height is overwritten with the actual distance from last to first line
        """
        return self.top - self.bottom 

           
    # ----------------------------------------
    

    @property
    def _reference_dimension(self):
        return self._end_point - self._start_point

    @property
    def subdivisions(self):
        return abs(int(self._reference_dimension // self.subdivision_dimension)) + 1
    
    @property
    def subdivision_dimension(self):
        """
        the absolute dimension of a single subdivision within the grid
        """
        return -self.line_height

    def span(self, span):
        """
        the absolute dimension of a span of consecutive subdivisions within the grid, 
        including their inbetween gutters
        """
        return span * self.subdivision_dimension

    # ----------------------------------------
    
    def __getitem__(self, index):
        if index >= 0:
            return self._start_point + index * self.subdivision_dimension
        else:
            return self._start_point + len(self) * self.subdivision_dimension + index * self.subdivision_dimension

    def __len__(self):
        return self.subdivisions

    def __iter__(self):
        return iter([self.__getitem__(i) for i in range(self.subdivisions)])

    # ----------------------------------------
    
    draw_color = (1, 0, 1, 1)

    def draw_frame(self):
        for c in self:
            db.line((self.left, c), (self.right, c))

    def draw_indexes(self):
        for i, line in enumerate(self):
            db.text(str(i), (self.left + 2, line+2))


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


def grid_textbox(txt, box, baselineGrid, align_first_line_only=False, align=None):

    with db.savedState():
        # textBlox does not like negative height
        box = correct_box_direction(box)

        x, y, w, h = box

        if not align_first_line_only:
            actual_line_height = db.fontLineHeight()
            target_line_height = math.ceil(actual_line_height / baselineGrid.line_height) * baselineGrid.line_height
            set_metric_line_height(target_line_height)

        # align cap height to the top of the box
        abs_cap_h = db.fontCapHeight()
        first_line_y = db.textBoxBaselines(txt, box)[0][1]
        current_cap_y = first_line_y + abs_cap_h
        cap_y_offset = y+h - current_cap_y

        # align top height of the text to the top of the box
        # first_piece_of_text = db.textBoxCharacterBounds(txt, box)[0]
        # top_of_text = first_piece_of_text.bounds[1] + first_piece_of_text.bounds[3]
        # top_of_text_offset = y+h - top_of_text
        # first_line_y = db.textBoxBaselines(txt, box)[0][1]
        # offset_first_line_y = first_line_y + top_of_text_offset
        #theoretical_first_line = y + h - db.fontLineHeight()

        first_line_y_with_cap_offset = first_line_y + cap_y_offset
        target_line_index = baselineGrid.baseline_index_from_coordinate(first_line_y_with_cap_offset)
        target_line = baselineGrid[target_line_index]

        offset = target_line - first_line_y

        # target_first_line = math.ceil(font_top / grid) * grid
        # actual_first_line = get_first_line_height_relative_to_box(txt, (x, y, w, h))
        # offset = actual_first_line - target_first_line
        # db.baselineShift(offset * BASELINE_SHIFT_RATIO_ADJUST)

        db.textBox(txt, (x, y+offset, w, h), align=align)


# def get_first_line_height_relative_to_box(txt, box):
#     x, y, w, h = box
#     absolute_first_line_x, absolute_first_line_y = db.textBoxBaselines(txt, box)[0]
#     relative_first_line_y = y + h - absolute_first_line_y
#     return relative_first_line_y

def get_first_line_height_relative_to_box(txt, box):
    first_line = db.textBoxBaselines(txt, box)[0]


def correct_box_direction(box):
    x, y, w, h = box
    if h < 0:
        y = y + h
        h = h * -1
    return(x, y, w, h)

# ----------------------------------------


def vertically_centered_text_box(text, box, align=None):
    with db.savedState():
        try:
            text = text.strip()
        except:
            pass
        x, y, w, h = correct_box_direction(box)
        font_top = db.fontCapHeight()
        
        lines = db.textBoxBaselines(text, (0, 0, w, h))

        if len(lines) > 0:
            top = lines[0][1] + font_top
            bottom = lines[-1][1]
            text_h = top - bottom
            margin = (h - text_h) / 2
            shift = margin - bottom
            #cdb.baselineShift(shift * BASELINE_SHIFT_RATIO_ADJUST)
            db.textBox(text, (x, y+shift, w, h), align=align)

# ----------------------------------------

def set_metric_line_height(line_height):
    txt = "H\nH"
    db.lineHeight(line_height)
    # should calculate appropriate size here
    lines = db.textBoxBaselines(txt, (0, 0, 10000, 10000))
    line_dist = lines[0][1] - lines[1][1]
    target_line_dist = line_height
    required_line_dist = target_line_dist - line_dist + target_line_dist
    db.lineHeight(required_line_dist)

