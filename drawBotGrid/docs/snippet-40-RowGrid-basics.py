from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import RowGrid

newPage("A4Landscape")

rows = RowGrid.from_margins((-50, -150, -50, -50), subdivisions=4, gutter=5)

fill(0, 1, 0, .5)  # green
for i in range(4):
    rect(rows.left, rows[i], rows.width*.5, rows*1)

fill(1, 0, 0, .5)  # red
rect(rows.right, rows[2], -rows.width*.5, rows*2)

fill(0, 1, 1, .5)  # cyan
rect(rows.right, rows[0], -rows.width*.25, rows*2)

rows.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
