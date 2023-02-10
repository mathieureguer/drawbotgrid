from drawBot import *
from drawBotGrid import ColumnGrid, RowGrid, Grid, BaselineGrid

import pathlib

def page_background():
    with savedState():
        fill(1)
        stroke(.5)
        rect(0, 0, width(), height())

# ----------------------------------------
# intro image

file_name = "columns_intro.png"

newPage("A4Landscape")
page_background()

columns = ColumnGrid((50, 50, 742, 495), subdivisions=8, gutter=10)

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
# basic coordinates

file_name = "columns_basic.png"

newPage("A4Landscape")
page_background()

columns = ColumnGrid((50, 50, 742, 495), subdivisions=8, gutter=10)

fill(0, 1, 0, .5)
rect(columns[0], 450, 50, 50)
rect(columns[1], 450, 50, 50)
rect(columns[2], 450, 50, 50)
rect(columns[3], 450, 50, 50)
rect(columns[4], 450, 50, 50)
rect(columns[5], 450, 50, 50)

fill(0, 1, 1, .5)
rect(columns[-1], 250, -50, 50)
rect(columns[-2], 250, -50, 50)
rect(columns[-3], 250, -50, 50)
rect(columns[-4], 250, -50, 50)
rect(columns[-5], 250, -50, 50)
rect(columns[-6], 250, -50, 50)

columns.draw(show_index=True)

out_path = pathlib.Path(__file__).parent / file_name
saveImage(out_path, imageResolution=144)

# ----------------------------------------
# magic multiplier and negative index

file_name = "columns_multiply.png"

newPage("A4Landscape")
page_background()

columns = ColumnGrid((50, 50, 742, 495), subdivisions=8, gutter=10)

fill(1, 0, 0, .5) 
rect(columns[0],  50, columns * 1, 100)
rect(columns[0], 170, columns * 3, 100)
rect(columns[0], 290, columns * 5, 100)
rect(columns[0], 410, columns * 7, 100)

fill(0, 1, 1, .5)
rect(columns[-1],  50, columns * -7, 100)
rect(columns[-1], 170, columns * -5, 100)
rect(columns[-1], 290, columns * -3, 100)
rect(columns[-1], 410, columns * -1, 100)

columns.draw(show_index=True)

out_path = pathlib.Path(__file__).parent / file_name
saveImage(out_path, imageResolution=144)

# ----------------------------------------
# init from margin 

file_name = "columns_margins.png"
newPage("A4Landscape")
page_background()
columns = ColumnGrid.from_margins((-20, -100, -50, -20), 6, 20)

columns.draw(show_index=True)
out_path = pathlib.Path(__file__).parent / file_name
saveImage(out_path, imageResolution=144)
