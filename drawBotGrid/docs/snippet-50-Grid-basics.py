from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import Grid

newPage("A4Landscape")

grid = Grid.from_margins((-50, -50, -50, -50), 
                         column_subdivisions=8, 
                         row_subdivisions=8, 
                         column_gutter=5, 
                         row_gutter=5)

fill(0, 1, 0, .5)  # green
for i in range(8):
    rect(grid.columns[0], grid.rows[i], grid.columns*1, grid.rows*1)

fill(0, 1, 1, .5)  # cyan
for i in range(1, 8):
    rect(grid.columns[i], grid.rows[-1], grid.columns*1, grid.rows*-2)

fill(1, 0, 0, .5) # red
rect(grid.columns[1], grid.rows[0], grid.columns*3, grid.rows*6)

fill(1, 0, 1, .5) # pink
rect(grid.columns[4], grid.rows[3], grid.columns*3, grid.rows*3)

grid.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
