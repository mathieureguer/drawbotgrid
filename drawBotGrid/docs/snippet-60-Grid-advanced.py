from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import Grid

newPage("A4Landscape")

grid = Grid.from_margins((-50, -50, -50, -50), 
                         column_subdivisions=12, 
                         row_subdivisions=4, 
                         column_gutter=5, 
                         row_gutter=5)

fill(0, 1, 0, .5)  # green
rect(*grid[(0, 0)], *grid*(3, 4))

fill(1, 0, 0, .5)  # red
rect(*grid[(3, -2)], *grid*(6, -3))

fill(1, 0, 1, .5) # pink
rect(*grid[(3, -1)], *grid*(3, -1))

fill(0, 1, 1, .5)  # cyan
rect(*grid[(9, -2)], *grid*(3, -2))

grid.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
