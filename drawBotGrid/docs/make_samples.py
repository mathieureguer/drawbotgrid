from drawBot import *
from drawBotGrid import ColumnGrid, RowGrid, Grid, BaselineGrid

import pathlib

# ----------------------------------------
# intro image

file_name = "columns_0.png"

newPage("A4Landscape")
columns = ColumnGrid((50, 50, 742, 495), 8, 10)

fill(0, 1, 0, .5)
rect(columns[1], columns.bottom, columns * 3, columns.height)

fill(1, 0, 0, .5) 
rect(columns[0], columns.top - 000, columns * 1, -100)
rect(columns[1], columns.top - 100, columns * 4, -100)
rect(columns[5], columns.top - 200, columns * 2, -100)

fill(0, 1, 1, .5)
rect(columns[-1], columns.bottom , columns * -4, 170)

columns.draw(show_index=True)

out_path = pathlib.Path(__file__).parent / file_name
saveImage(out_path, imageResolution=144)

# ----------------------------------------
# basic coordinate

file_name = "columns_1.png"

newPage("A4Landscape")
columns = ColumnGrid((50, 50, 742, 495), 8, 10)

fill(0, 1, 0, .5)
rect(columns[1], 100, columns * 3, 300)

columns.draw(show_index=True)

out_path = pathlib.Path(__file__).parent / file_name
saveImage(out_path, imageResolution=144)

# ----------------------------------------
# magic multiplier and negative index

file_name = "columns_2.png"

newPage("A4Landscape")
columns = ColumnGrid((50, 50, 742, 495), 8, 10)

fill(1, 0, 0, .5) 
rect(columns[0], columns.top - 000, columns * 1, -100)
rect(columns[0], columns.top - 120, columns * 3, -100)
rect(columns[0], columns.top - 240, columns * 5, -100)
rect(columns[0], columns.top - 360, columns * 7, -100)

fill(0, 1, 1, .5)
rect(columns[-1], columns.top - 000, columns * -7, -100)
rect(columns[-1], columns.top - 120, columns * -5, -100)
rect(columns[-1], columns.top - 240, columns * -3, -100)
rect(columns[-1], columns.top - 360, columns * -1, -100)

columns.draw(show_index=True)

out_path = pathlib.Path(__file__).parent / file_name
saveImage(out_path, imageResolution=144)

# ----------------------------------------
# init from margin 

file_name = "columns_3.png"
newPage("A4Landscape")
columns = ColumnGrid.from_margins((-20, -100, -50, -20), 6, 20)

columns.draw(show_index=True)
out_path = pathlib.Path(__file__).parent / file_name
saveImage(out_path, imageResolution=144)
