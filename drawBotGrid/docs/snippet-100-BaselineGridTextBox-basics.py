from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import ColumnGrid, BaselineGrid, baselineGridTextBox

newPage("A4Landscape")

# </include> ----------------------------------------
fill(1, 1, 1, .5)
rect(0, 0, width(), height())
# <include> ----------------------------------------

baselines = BaselineGrid.from_margins((0, 0, 0, 0), 
                         line_height=12)
columns = ColumnGrid((50, baselines[-4], width()-100, baselines*-44), subdivisions=3)

fill(0)
font("Georgia")
fontSize(9)
lineHeight(11.5)
textBox("This is a classic textBox.\n" + "blah "*1000, 
        (columns[0], columns.bottom, columns*1, columns.height))

baselineGridTextBox("This is a classic baselineGridTextBox.\n" + "blah "*1000, 
                    (columns[1], columns.bottom, columns*1, columns.height),
                    baselines)

baselineGridTextBox("This is a classic baselineGridTextBox\nwith align_first_line_only set to True.\n" + "blah "*1000, 
                    (columns[2], columns.bottom, columns*1, columns.height),
                    baselines,
                    align_first_line_only=True)

baselines.draw(show_index=True)
columns.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
