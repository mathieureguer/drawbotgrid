from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import ColumnGrid, verticalAlignTextBox

newPage("A4Landscape")

# </include> ----------------------------------------
with savedState():
    fill(1, 1, 1, .5)
    rect(0, 0, width(), height())
# <include> ----------------------------------------

columns = ColumnGrid.from_margins((-50, -150, -50, -150), subdivisions=3, gutter=10)

font("Georgia")
fontSize(34)
lineHeight(40)

verticalAlignTextBox("HELLO\nFROM UP\nTHERE", 
                     (columns[0], columns.bottom, columns*1, columns.height),
                     vertical_align="top",
                     align="center")

verticalAlignTextBox("HELLO\nFROM MID\nTHERE", 
                     (columns[1], columns.bottom, columns*1, columns.height),
                     vertical_align="center",
                     align="center")

verticalAlignTextBox("HELLO\nFROM DOWN\nTHERE", 
                     (columns[2], columns.bottom, columns*1, columns.height),
                     vertical_align="bottom",
                     align="center")

columns.draw(show_index=True)

# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
