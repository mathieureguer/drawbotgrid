from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import ColumnGrid

newPage("A4Landscape")

columns = ColumnGrid((50, 50, 742, 495), subdivisions=8, gutter=10)

fill(0, 1, 0, .5)
rect(columns[1], columns.bottom, columns*3, columns.height)

fill(1, 0, 0, .5) 
rect(columns[0], columns.top - 000, columns*1, -100)
rect(columns[1], columns.top - 100, columns*4, -100)
rect(columns[5], columns.top - 200, columns*2, -100)

fill(0, 1, 1, .5)
rect(columns[-1], columns.bottom , columns*-4, 170)

columns.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)