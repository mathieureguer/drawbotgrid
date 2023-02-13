from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import ColumnGrid, BaselineGrid, baselineGridTextBox

newPage("A4Landscape")

baselines = BaselineGrid.from_margins((0, 0, 0, 0), 
                         line_height=6)
columns = ColumnGrid((50, baselines[-8], width()-100, baselines*-88), subdivisions=3)

fill(0)
font("Georgia")
fontSize(5)
lineHeight(6)
baselineGridTextBox("BaselineGrid: 6pt\nFont Size 5pt\nLine Height: 6pt\n" + "blah "*1000, 
                    (columns[0], columns.bottom, columns*1, columns.height),
                    baselines)

fontSize(10)
lineHeight(10)
baselineGridTextBox("BaselineGrid: 6pt\nFont Size 10pt\nLine Height: 10pt\n" + "blah "*1000, 
                    (columns[1], columns.bottom, columns*1, columns.height),
                    baselines)

fontSize(16)
lineHeight(18)
baselineGridTextBox("BaselineGrid: 6pt\nFont Size 16pt\nLine Height: 18pt\n" + "blah "*1000, 
                    (columns[2], columns.bottom, columns*1, columns.height),
                    baselines)


baselines.draw(show_index=True)
columns.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
