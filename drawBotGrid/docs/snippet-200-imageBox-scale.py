
from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import Grid, imageBox

newPage("A4Landscape")

grid = Grid.from_margins((-60, -40, -60, -40), column_subdivisions=3, row_subdivisions=3)


img_path = "https://raw.githubusercontent.com/mathieureguer/drawbotgrid/main/drawBotGrid/docs/drawMech-small.jpg"

imageBox(img_path, (grid.columns[0], grid.rows[2], grid.columns*1, grid.rows*1), fitting="crop", scale= .5, anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[1], grid.rows[2], grid.columns*1, grid.rows*1), fitting="crop", scale= .6, anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[2], grid.rows[2], grid.columns*1, grid.rows*1), fitting="crop", scale= .7, anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[0], grid.rows[1], grid.columns*1, grid.rows*1), fitting="crop", scale= .8, anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[1], grid.rows[1], grid.columns*1, grid.rows*1), fitting="crop", scale= .9, anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[2], grid.rows[1], grid.columns*1, grid.rows*1), fitting="crop", scale=1  , anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[0], grid.rows[0], grid.columns*1, grid.rows*1), fitting="crop", scale=1.2, anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[1], grid.rows[0], grid.columns*1, grid.rows*1), fitting="crop", scale=1.4, anchor=("right", "top"), draw_box_frame=True)
imageBox(img_path, (grid.columns[2], grid.rows[0], grid.columns*1, grid.rows*1), fitting="crop", scale=1.6, anchor=("right", "top"), draw_box_frame=True)

# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
