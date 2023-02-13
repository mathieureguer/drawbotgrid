from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import ColumnGrid

newPage("A4Landscape")

columns = ColumnGrid((50, 50, 742, 495), subdivisions=8, gutter=10)

fill(1, 0, 0, .5)  # red
rect(columns[0],  50, columns*1, 100)
rect(columns[0], 170, columns*3, 100)
rect(columns[0], 290, columns*5, 100)
rect(columns[0], 410, columns*7, 100)

fill(0, 1, 1, .5) # cyan
rect(columns[-1],  50, columns*-7, 100)
rect(columns[-1], 170, columns*-5, 100)
rect(columns[-1], 290, columns*-3, 100)
rect(columns[-1], 410, columns*-1, 100)

columns.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
