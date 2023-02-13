from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import ColumnGrid

newPage("A4Landscape")

columns = ColumnGrid.from_margins((-20, -100, -20, -50), subdivisions=6, gutter=20)

fill(0, 1, 1, .5) # cyan
rect(columns[0], columns.bottom, columns*3, columns.height)
fill(0, 1, 0, .5) # green
rect(columns[3], columns.top, columns*3, columns.height*-.5)

columns.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
