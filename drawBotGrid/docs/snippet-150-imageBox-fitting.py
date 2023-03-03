
from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import ColumnGrid, imageBox

newPage("A4Landscape")

font("Georgia")
fontSize(14)
columns = ColumnGrid.from_margins((-50, -80, -50, -80), subdivisions=3)

img_path = "/Users/mathieu/Dropbox/20 current dev/Custom Modules/DrawBotGrid/drawBotGrid/docs/drawMech-small.jpg"
imageBox(img_path, (columns[0], columns.bottom, columns*1, columns.height), fitting="crop", anchor=("center", "top"))
textBox('fitting="crop"', (columns[0], columns.bottom-40, columns*1, 30), align="center")

imageBox(img_path, (columns[1], columns.bottom, columns*1, columns.height), fitting="fill", anchor=("center", "top"))
textBox('fitting="fill"', (columns[1], columns.bottom-40, columns*1, 30), align="center")

imageBox(img_path, (columns[2], columns.bottom, columns*1, columns.height), fitting="fit", anchor=("center", "top"))
textBox('fitting="fit"', (columns[2], columns.bottom-40, columns*1, 30), align="center")

columns.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
