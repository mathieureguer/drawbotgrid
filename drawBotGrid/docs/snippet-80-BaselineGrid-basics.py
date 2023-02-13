from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import BaselineGrid

newPage("A4Landscape")

baselines = BaselineGrid.from_margins((-50, -50, -50, -50), 
                         line_height=12)

fill(1, 0, 0, .5) # red
item_width = baselines.width / len(baselines)
for i in range(len(baselines)):
    rect(baselines.left+item_width*i, baselines[i], item_width, baselines*1)

baselines.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
