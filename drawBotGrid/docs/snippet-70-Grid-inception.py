from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import Grid

newPage("A4Landscape")

main_grid = Grid.from_margins((-50, -50, -50, -50), 
                         column_subdivisions=3, 
                         row_subdivisions=2, 
                         column_gutter=5, 
                         row_gutter=5)

sub_grid = Grid((main_grid.columns[2], main_grid.rows[1], main_grid.columns*1, main_grid.rows*1),
                column_subdivisions=4, 
                row_subdivisions=6, 
                column_gutter=5, 
                row_gutter=5)


other_sub_grid = Grid((main_grid.columns[2], main_grid.rows[0], main_grid.columns*1, main_grid.rows*1),
                       column_subdivisions=2, 
                       row_subdivisions=3, 
                       column_gutter=5, 
                       row_gutter=5)



main_grid.draw(show_index=True)
sub_grid.draw(show_index=True)
other_sub_grid.draw(show_index=True)
# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
