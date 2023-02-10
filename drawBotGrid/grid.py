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
        assert isinstance(span, (float, int))
        if span >= 0:
            return self.subdivision_dimension * span + self.gutter * (math.ceil(span) - 1)
        else:
            return self.subdivision_dimension * span + self.gutter * (math.ceil(span) + 1)
    
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

    def __mul__(self, factor):
        return self.span(factor) 

    
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

    def span(self, column_span_row_span):
        """
        the absolute dimension of a span of consecutive subdivision within the grid, including their inbetween gutters
        """
        assert len(column_span_row_span) == 2
        column_span, row_span = column_span_row_span
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
    
    def baseline_index_from_coordinate(self, y_coordinate):
        for i, line in enumerate(self):
            if y_coordinate >= line:
                return i

    def closest_line_below_coordinate(self, y_coordinate):
        for i, line in enumerate(self):
            if y_coordinate >= line:
                return line

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
    
    draw_color = (0, 1, 1, 1)

    def draw_frame(self):
        for c in self:
            db.line((self.left, c), (self.right, c))

    def draw_indexes(self):
        for i, line in enumerate(self):
            db.text(str(i), (self.left + 2, line+2))
