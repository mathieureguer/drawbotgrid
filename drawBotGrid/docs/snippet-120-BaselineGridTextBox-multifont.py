from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import Grid, BaselineGrid, baselineGridTextBox

newPage("A4Landscape")

baselines = BaselineGrid.from_margins((0, 0, 0, 0), 
                         line_height=12)
grid = Grid((50, baselines[-4], width()-100, baselines*-44), column_subdivisions=3, row_subdivisions=2)


fill(0)
font("Obviously")
fontSize(10)
lineHeight(12)
textBox("Helvetica: 10/12pt\n" + "blah "*1000, 
                    (grid.columns[0], grid.rows[1], grid.columns*1, grid.rows*1))

fill(0)
font("Georgia")
fontSize(10)
lineHeight(12)
textBox("Georgia: 10/12pt\n" + "blah "*1000, 
                    (grid.columns[1], grid.rows[1], grid.columns*1, grid.rows*1))

fill(0)
font("Verdana")
fontSize(10)
lineHeight(12)
textBox("Verdana: 10/12pt\n" + "blah "*1000, 
                    (grid.columns[2], grid.rows[1], grid.columns*1, grid.rows*1))



fill(0)
font("Obviously")
fontSize(10)
lineHeight(12)
baselineGridTextBox("Helvetica: 10/12pt\n" + "blah "*1000, 
                    (grid.columns[0], grid.rows[0], grid.columns*1, grid.rows*1),
                    baselines)

fill(0)
font("Georgia")
fontSize(10)
lineHeight(12)
baselineGridTextBox("Georgia: 10/12pt\n" + "blah "*1000, 
                    (grid.columns[1], grid.rows[0], grid.columns*1, grid.rows*1),
                    baselines)

fill(0)
font("Verdana")
fontSize(10)
lineHeight(12)
baselineGridTextBox("Verdana: 10/12pt\n" + "blah "*1000, 
                    (grid.columns[2], grid.rows[0], grid.columns*1, grid.rows*1),
                    baselines)


baselines.draw(show_index=True)
grid.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
