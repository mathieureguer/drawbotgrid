
from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import Grid, imageBox

newPage("A4Landscape")

grid = Grid.from_margins((-50, -50, -50, -50), column_subdivisions=10, row_subdivisions=6)
grid.draw()

img_path = "https://raw.githubusercontent.com/mathieureguer/drawbotgrid/main/drawBotGrid/docs/drawMech-small.jpg"
imageBox(img_path, (grid.columns[0], grid.rows[0], grid.columns*4, grid.rows*4), draw_box_frame=True, fitting="crop", anchor=("center", "top"))
imageBox(img_path, (grid.columns[0], grid.rows[4], grid.columns*4, grid.rows*2), draw_box_frame=True, fitting="crop", anchor=("center", "top"))
imageBox(img_path, (grid.columns[4], grid.rows[0], grid.columns*3, grid.rows*4), draw_box_frame=True, fitting="crop", anchor=("center", "top"))
imageBox(img_path, (grid.columns[7], grid.rows[0], grid.columns*3, grid.rows*3), draw_box_frame=True, fitting="crop", anchor=("center", "top"))
imageBox(img_path, (grid.columns[7], grid.rows[3], grid.columns*3, grid.rows*2), draw_box_frame=True, fitting="crop", anchor=("center", "top"))
imageBox(img_path, (grid.columns[4], grid.rows[4], grid.columns*2, grid.rows*2), draw_box_frame=True, fitting="crop", anchor=("center", "top"))
imageBox(img_path, (grid.columns[6], grid.rows[4], grid.columns*1, grid.rows*2), draw_box_frame=True, fitting="crop", anchor=("center", "top"))
imageBox(img_path, (grid.columns[7], grid.rows[5], grid.columns*3, grid.rows*1), draw_box_frame=True, fitting="crop", anchor=("center", "top"))


# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
