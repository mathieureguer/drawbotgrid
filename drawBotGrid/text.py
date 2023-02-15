import drawBot as db
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
        db.textBox(txt, (x, y+shift, w, h), align=align)

baselineGridTextBox = baseline_grid_textBox

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
