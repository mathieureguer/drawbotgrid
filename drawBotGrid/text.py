import drawBot as db
from .grid import ColumnGrid
import math

# ----------------------------------------

def baseline_grid_textBox(txt, 
                box, 
                baseline_grid, 
                align_first_line_only=False, 
                align="left"):

    with db.savedState():
        box = correct_box_direction(box)

        x, y, w, h = box

        if not align_first_line_only:
            actual_line_height = db.fontLineHeight()
            target_line_height = math.ceil(actual_line_height / baseline_grid.line_height) * baseline_grid.line_height
            set_metric_baseline_height(target_line_height)

        absolute_cap_height = db.fontCapHeight()
        first_line_y = db.textBoxBaselines(txt, box)[0][1]
        current_cap_y = first_line_y + absolute_cap_height
        cap_distance_from_top = y + h - current_cap_y

        highest_possible_first_line = first_line_y + cap_distance_from_top
        target_line = baseline_grid.closest_line_below_coordinate(highest_possible_first_line)

        shift = target_line - first_line_y
        overflow = db.textBox(txt, (x, y+shift, w, h), align=align)
        return overflow

baselineGridTextBox = baseline_grid_textBox

# ----------------------------------------

def column_textBox(txt, box, subdivisions=2, gutter=10, align="left", draw_grid=False):
    _column_textBox_base(txt, box, baseline_grid=None, align_first_line_only=False, subdivisions=subdivisions, gutter=gutter, align=align, draw_grid=draw_grid)

columnTextBox = column_textBox


def column_baseline_grid_textBox(txt, box, baseline_grid, align_first_line_only=False, subdivisions=2, gutter=10, align="left", draw_grid=False):
    _column_textBox_base(txt, box, baseline_grid, align_first_line_only=align_first_line_only, subdivisions=subdivisions, gutter=gutter, align=align, draw_grid=draw_grid)

columnBaselineGridTextBox = column_baseline_grid_textBox


def _column_textBox_base(txt, 
                         box, 
                         baseline_grid=None,
                         align_first_line_only=False,
                         subdivisions=2, 
                         gutter=10, 
                         align="left", 
                         draw_grid=False):

    columns = ColumnGrid(box, subdivisions=subdivisions, gutter=gutter)
    overflow = txt
    for col in columns:
        if len(overflow) > 0:
            sub_box = (col, columns.bottom, columns*1, columns.height)
            if baseline_grid:
                overflow = baseline_grid_textBox(overflow, 
                                                    sub_box, 
                                                    baseline_grid,
                                                    align=align)
            else:
                overflow = db.textBox(overflow, 
                                      sub_box, 
                                      align=align)

    if draw_grid:
        grid_color =  (.5, 0, .8, 1)
        with db.savedState():
            db.strokeWidth(.5)
            
            db.fill(None)
            db.stroke(*grid_color)
            db.rect(*box)

            for col in columns[1:]:
                db.fill(None)
                db.stroke(*grid_color)
                db.line((col-columns.gutter, columns.bottom), (col-columns.gutter, columns.top))
                db.line((col, columns.bottom), (col, columns.top))

            for col in columns[1:]:
                db.fill(None)
                db.stroke(*grid_color)
                start_pt = (col-columns.gutter, columns.bottom)
                end_pt = (col, columns.top)
                text_flow_path = _get_text_flow_path(start_pt, end_pt)
                db.drawPath(text_flow_path)
                
                db.stroke(None)
                db.fill(*grid_color)
                _draw_point(start_pt, radius=4)
                _draw_point(end_pt, radius=4)
        
    return overflow

# ----------------------------------------

def _get_text_flow_path(xy1, xy2):
    x_1, y_1 = xy1
    x_2, y_2 = xy2
    off_curve_length = 100
    text_flow_path = db.BezierPath()
    text_flow_path.moveTo( (x_1, y_1))
    text_flow_path.curveTo((x_1+off_curve_length, y_1),
                           (x_2-off_curve_length, y_2),
                           (x_2, y_2))
    return text_flow_path

def _draw_point(xy, radius=2):
    x, y = xy
    db.oval(x-radius, y-radius, radius*2, radius*2)

# ----------------------------------------

def vertically_centered_textBox(text, box, align=None):
        if len(text) > 0:
            text = text.strip()

        x, y, w, h = correct_box_direction(box)
        font_top = db.fontCapHeight()        
        lines = db.textBoxBaselines(text, (0, 0, w, h))

        if len(lines) > 0:
            top = lines[0][1] + font_top
            bottom = lines[-1][1]
            text_h = top - bottom
            margin = (h - text_h) / 2
            shift = margin - bottom
            db.textBox(text, (x, y+shift, w, h), align=align)

verticallyCenteredTextBox = vertically_centered_textBox

# ----------------------------------------

def set_metric_baseline_height(line_height):
    # Wait a minute. I am not sure that's necessary. Will investigate.
    txt = "H\nH"
    db.lineHeight(line_height)

    # should calculate appropriate size here
    lines = db.textBoxBaselines(txt, (0, 0, 10000, 10000))
    line_dist = lines[0][1] - lines[1][1]
    target_line_dist = line_height
    required_line_dist = target_line_dist - line_dist + target_line_dist
    db.lineHeight(required_line_dist)

baselineHeight = set_metric_baseline_height

# ----------------------------------------

def correct_box_direction(box):
    x, y, w, h = box
    if h < 0:
        y = y + h
        h = h * -1
    return(x, y, w, h)

# ----------------------------------------

def image_at_size(path, box, preserve_proprotions=True):
    """
    this could do a lot more. 
    Things like cropping the image, 
    aligning it somewhere esle that bottom, left...
    """
    x, y, w, h = box
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

imageBox = image_at_size
