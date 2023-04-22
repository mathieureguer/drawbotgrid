import drawBot as db
import pathlib
import tempfile
import PIL

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

imageAtSize = image_at_size

# ----------------------------------------

def image_box(path,
             box,
             fitting="fit",
             scale=1,
             anchor=("left", "top"),
             draw_box_frame=False,
             **kwargs):

    assert fitting in ("fit", "fill", "crop")

    im_path = pathlib.Path(path)
    with tempfile.NamedTemporaryFile(suffix=im_path.suffix, delete=False) as im_cropped:

        x, y, w, h = box
        
        # get the scale ratio
        image_w, image_h = db.imageSize(path)
        scale_ratio_w = w / image_w
        scale_ratio_h = h / image_h
        if fitting == "fit":
            scale_ratio = min(scale_ratio_w, scale_ratio_h)
        elif fitting == "fill":
            scale_ratio = max(scale_ratio_w, scale_ratio_h)
        elif fitting == "crop":        
            scale_ratio = scale

        _crop_image_with_anchor(path, im_cropped.name, anchor, w/scale_ratio, h/scale_ratio)

        im_width, im_height = db.imageSize(im_cropped.name)
        im_width_scaled = im_width*scale_ratio
        im_height_scaled = im_height*scale_ratio
        anchor_x, anchor_y = anchor

        if anchor_x == "left":
            offset_x = x
        elif anchor_x == "right":
            offset_x = x + w - im_width_scaled
        elif anchor_x == "center":
            offset_x = x + (w - im_width_scaled)/2

        assert anchor_y in ("center", "bottom", "top")
        if anchor_y == "bottom":
            offset_y = y
        elif anchor_y == "top":
            offset_y = y + h - im_height_scaled
        elif anchor_y == "center":
            offset_y = y + (h - im_height_scaled)/2

        with db.savedState():
            db.translate(offset_x, offset_y)
            db.scale(scale_ratio, scale_ratio)
            db.image(im_cropped.name, (0, 0), **kwargs)

        if draw_box_frame:
            grid_color =  (.5, 0, .8, 1)
            with db.savedState():
                db.strokeWidth(.5)
                db.fill(None)
                db.stroke(*grid_color)
                db.rect(*box)

def _crop_image_with_anchor(input_path, output_path, anchor, crop_width, crop_height):
    
    anchor_x, anchor_y = anchor
    im_width, im_height = db.imageSize(input_path)
    if anchor_x == "left":
        crop_x = 0
    elif anchor_x == "right":
        crop_x = im_width - crop_width
    elif anchor_x == "center":
        crop_x = (im_width - crop_width)/2

    if anchor_y == "bottom":
        crop_y = 0
    elif anchor_y == "top":
        crop_y = im_height- crop_height
    elif anchor_y == "center":
        crop_y = (im_height - crop_height)/2

    ## moving through PIL here
    ## as drawBot imageObject.crop 
    ## seems to produce blurred borders

    im = PIL.Image.open(input_path)
    im = im.crop((crop_x, crop_y, crop_x+crop_width, crop_y+crop_height))
    im.save(output_path)

# def _get_image_offset_in_box(im, box, anchor):
#     x, y, w, h = box
#     anchor_x, anchor_y = anchor
#     im_width, im_height = db.imageSize(im)
#     if anchor_x == "left":
#         offset_x = x
#     elif anchor_x == "right":
#         offset_x = x + w - im_width
#     elif anchor_x == "center":
#         offset_x = x + (w - im_width)/2

#     assert anchor_y in ("center", "bottom", "top")
#     if anchor_y == "bottom":
#         offset_y = y
#     elif anchor_y == "top":
#         offset_y = y + h - im_height
#     elif anchor_y == "center":
#         offset_y = y + (h - im_height)/2

#     return (offset_x, offset_y)

imageBox = image_box