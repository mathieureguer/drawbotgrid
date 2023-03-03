
from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import Grid, ColumnGrid, imageBox

newPage("A4Landscape")

global_grid = ColumnGrid.from_margins((-60, -40, -60, -40), subdivisions=2, gutter=40)
grid_left = Grid((global_grid[0], global_grid.bottom, global_grid*1, global_grid.height), column_subdivisions=3, row_subdivisions=3)
grid_right= Grid((global_grid[1], global_grid.bottom, global_grid*1, global_grid.height), column_subdivisions=3, row_subdivisions=3)

img_path = "https://raw.githubusercontent.com/mathieureguer/drawbotgrid/main/drawBotGrid/docs/drawMech-small.jpg"

imageBox(img_path, (grid_left.columns[0], grid_left.rows[0], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("left", "bottom"), draw_box_frame=True)
imageBox(img_path, (grid_left.columns[0], grid_left.rows[1], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("left", "center"), draw_box_frame=True)
imageBox(img_path, (grid_left.columns[0], grid_left.rows[2], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("left", "top"), draw_box_frame=True)

imageBox(img_path, (grid_left.columns[1], grid_left.rows[0], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("center", "bottom"), draw_box_frame=True)
imageBox(img_path, (grid_left.columns[1], grid_left.rows[1], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("center", "center"), draw_box_frame=True)
imageBox(img_path, (grid_left.columns[1], grid_left.rows[2], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("center", "top"), draw_box_frame=True)

imageBox(img_path, (grid_left.columns[2], grid_left.rows[0], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("right", "bottom"), draw_box_frame=True)
imageBox(img_path, (grid_left.columns[2], grid_left.rows[1], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("right", "center"), draw_box_frame=True)
imageBox(img_path, (grid_left.columns[2], grid_left.rows[2], grid_left.columns*1, grid_left.rows*1), fitting="crop", scale=.15, anchor=("right", "top"), draw_box_frame=True)

imageBox(img_path, (grid_right.columns[0], grid_right.rows[0], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("left", "bottom"), draw_box_frame=True)
imageBox(img_path, (grid_right.columns[0], grid_right.rows[1], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("left", "center"), draw_box_frame=True)
imageBox(img_path, (grid_right.columns[0], grid_right.rows[2], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("left", "top"), draw_box_frame=True)

imageBox(img_path, (grid_right.columns[1], grid_right.rows[0], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("center", "bottom"), draw_box_frame=True)
imageBox(img_path, (grid_right.columns[1], grid_right.rows[1], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("center", "center"), draw_box_frame=True)
imageBox(img_path, (grid_right.columns[1], grid_right.rows[2], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("center", "top"), draw_box_frame=True)

imageBox(img_path, (grid_right.columns[2], grid_right.rows[0], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("right", "bottom"), draw_box_frame=True)
imageBox(img_path, (grid_right.columns[2], grid_right.rows[1], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("right", "center"), draw_box_frame=True)
imageBox(img_path, (grid_right.columns[2], grid_right.rows[2], grid_right.columns*1, grid_right.rows*1), fitting="crop", scale=1, anchor=("right", "top"), draw_box_frame=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
