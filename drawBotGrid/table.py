import drawBot as db
from . import grid, text

from collections import UserList
import math


class Table:
    def __init__(self, possize, items, column_descriptions,
                 base_row_height=12,
                 margins=6,
                 header_gap=0):
        self.x, self.y, self.width, self.input_height = possize
        self.margins = margins

        self.columns_manager = ColumnsManager(self, column_descriptions)
        self.rows_manager = RowsManager(self, items,
                                        base_row_height=base_row_height, header_gap=header_gap)

        self.actual_height = self.rows_manager.total_height
        self.vertical_align = False

    # drawers

    def draw_columns_lines(self):
        for x in self.columns_manager.separator_origins:
            db.line((x, self.y), (x, self.y + self.height))

    def draw_rows_lines(self):
        for y in self.rows_manager.separator_origins:
            db.line((self.x, y), (self.x + self.width, y))

    def draw_frame(self):
        db.rect(self.x, self.y, self.width, self.height)

    def draw_rows_frame(self):
        db.line((self.x, self.y), (self.x + self.width, self.y))
        db.line((self.x, self.y+self.height), (self.x + self.width, self.y+self.height))

    def draw_columns_frame(self):
        db.line((self.x, self.y), (self.x, self.y+self.height))
        db.line((self.x+self.width, self.y), (self.x+self.width, self.y+self.height))

    def draw_content(self):
        for contents, cells in zip(self.cell_values, self.cell_rects):
            for content, cell in zip(contents, cells):
                if self.vertical_align:
                    text.verticalAlignTextBox(content, cell.raw_textbox, vertical_align="center")
                else:
                    db.textBox(content, cell.textbox)

    def draw_header_background(self):
        db.rect(*self.header_rect)

    def draw_content_background(self):
        db.rect(*self.content_rect)

    # properties

    @property
    def show_header(self):
        return self._show_header

    @show_header.setter
    def show_header(self, value):
        self._show_header = value
        self.rows_manager.show_header = value
    

    @property
    def height(self):
        return -self.rows_manager.total_height

    @property
    def cell_rects(self):
        out = []
        for y, height in zip(self.rows_manager.origins, self.rows_manager.heights):
            row = []
            for x, width in zip(self.columns_manager.origins, self.columns_manager.widths):
                row.append(CellBox(self, (x, y, width, height)))
            out.append(row)
        return out

    @property
    def cell_values(self):
        return self.rows_manager.cell_values

    @property
    def table_rect(self):
        return self.rows_manager.table_rect

    @property
    def header_rect(self):
        return self.rows_manager.header_rect

    @property
    def content_rect(self):
        return self.rows_manager.content_rect

    @property
    def content_rects(self):
        return self.rows_manager.content_rects


class ColumnsManager:

    WIDTH_KEY = "width"
    TITLE_KEY = "title"
    LABEL_KEY = "label"

    def __init__(self, parent, column_descriptions):
        self.table = parent
        self.column_descriptions = column_descriptions

        self.widths = self._calculate_columns_widths()
        self.origins = self._calculate_columns_origins()

        self.titles = self._get_column_descriptions_filtered_key()

    @property
    def rects(self):
        return [(x, self.table.y, w, self.table.height) for x, w in zip(self.origins, self.widths)]

    @property
    def separator_origins(self):
        return self.origins[1:]

    # ----------------------------------------
    # coordinates helpers

    def _get_number_of_flex_columns_width(self):
        return len([col for col in self.column_descriptions if col.get(self.WIDTH_KEY) == None])

    def _get_sum_of_defined_columns_width(self):
        return sum([col.get(self.WIDTH_KEY,  0) for col in self.column_descriptions])

    def _calculate_flex_width(self):
        return (self.table.width - self._get_sum_of_defined_columns_width()) / max(1, self._get_number_of_flex_columns_width())

    def _calculate_columns_widths(self):
        widths = []
        flex_width = self._calculate_flex_width()
        for col in self.column_descriptions:
            width = col.get(self.WIDTH_KEY, flex_width)
            widths.append(width)
        return widths

    def _calculate_columns_origins(self):
        origins = []
        current_x = self.table.x
        for width in self.widths:
            origins.append(current_x)
            current_x += width
        return origins

    # ----------------------------------------
    # content helpers

    def _get_column_descriptions_filtered_key(self):
        return [i[self.TITLE_KEY] for i in self.column_descriptions]

    def get_column_labels(self):
        return [i.get(self.LABEL_KEY, i[self.TITLE_KEY]) for i in self.column_descriptions]

    def filter_row_content(self, row):
        return [row.get(k, "") for k in self.titles]


class RowsManager:

    def __init__(self, parent, rows, base_row_height=12, header_gap=0):
        self.table = parent
        self.rows = [self.table.columns_manager.get_column_labels()] + self.filter_rows_content(rows)
        self.base_row_height = base_row_height
        self.header_gap = header_gap

        self._show_header = True

        self.heights = self._calculate_rows_heights()
        self.origins = self._calculate_rows_origins()


    @property
    def show_header(self):
        return self._show_header

    @show_header.setter
    def show_header(self, value):
        self._show_header = value
        self.heights = self._calculate_rows_heights()
        self.origins = self._calculate_rows_origins()

    @property
    def rects(self):
        return [(self.table.x, y, self.table.width, h) for y, h in zip(self.origins, self.heights)]

    @property
    def separator_origins(self):
        return self.origins[:-1]

    @property
    def total_height(self):
        return -self.origins[-1] + self.table.y

    @property
    def content_height(self):
        return sum(self.heights[1:])

    @property
    def header_rect(self):
        return (self.table.x, self.origins[0], self.table.width, self.heights[0])

    @property
    def content_rect(self):
        return (self.table.x, self.origins[-1], self.table.width, self.content_height)

    @property
    def content_rects(self):
        return [(self.table.x, y, self.table.width, h) for y, h in zip(self.origins[1:], self.heights[1:])]

    @property
    def table_rect(self):
        return (self.table.x, self.origins[-1], self.table.width, self.total_height)

    # ----------------------------------------

    @property
    def content_values(self):
        return self.rows[1:]

    @property
    def header_values(self):
        return self.rows[0]

    @property
    def cell_values(self):
        if self.show_header:
            return self.rows
        else:
            return self.content_values

    # ----------------------------------------
    # coordinate helpers

    def filter_rows_content(self, rows):
        return [self.table.columns_manager.filter_row_content(row) for row in rows]

    def _calculate_rows_heights(self):
        heights = []
        if self.show_header:
            rows = self.rows
        else:
            rows = self.rows[1:]
        for row in rows:
            heights.append(self._calculate_row_height(row))
        return heights

    def _calculate_rows_origins(self):
        origins = []
        current_y = self.table.y
        for i, height in enumerate(self.heights):
            if i == 1 and self.show_header:
                # second line might be lower than normal due to header gap
                current_y -= height + self.header_gap
            else:
                current_y -= height
            origins.append(current_y)
        return origins

    def _calculate_cell_height(self, content, width):
        return db.textSize(content, width=width)[1]

    def _calculate_row_height(self, row):
        vert_margin = (self.base_row_height - db.fontLineHeight()) / 2
        heights = []
        for content, width in zip(row, self.table.columns_manager.widths):
            heights.append(self._calculate_cell_height(content, width - self.table.margins * 2))
        max_height = max(heights)
        # return math.ceil(max_height / self.base_row_height) * self.base_row_height
        return max(max_height + vert_margin * 2, self.base_row_height)

class CellBox:

    def __init__(self, parent, possize):
        self.table = parent
        self.x, self.y, self.width, self.height = possize

    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)

    @property
    def textbox(self):
        offset = self._get_text_vertical_offset()
        return (self.x + self.table.margins, self.y - offset, self.width - self.table.margins * 2, self.height)

    @property
    def raw_textbox(self):
        return (self.x + self.table.margins, self.y, self.width - self.table.margins * 2, self.height)

    # ----------------------------------------

    def _get_text_vertical_offset(self):
        row_height = self.table.rows_manager.base_row_height
        # calculate first line offset
        font_top = db.fontCapHeight()
        target_first_line = row_height - (row_height - font_top) / 2 - font_top
        actual_first_line_x, actual_first_line_y = db.textBoxBaselines("H", (0, 0, 100, row_height))[0]
        offset = actual_first_line_y - target_first_line
        return offset
