from utils.input_box import IntegerInputBox, FloatInputBoxHoriLabel
import pyscratch as pysc
from settings import *

xpos1 = 830
xpos2 = 1050

offset_x_input = IntegerInputBox('offset_x', 'offset_x_change', "0", 80)
offset_x_input.set_xy((xpos1, 605))


offset_y_input = IntegerInputBox('offset_y', 'offset_y_change', "0", 80)
offset_y_input.set_xy((xpos2, 605))


row_input = IntegerInputBox('n_row', "n_row_change", "", 80)
row_input.set_xy((xpos1, 650))

col_input = IntegerInputBox('n_col', "n_col_change", "", 80)
col_input.set_xy((xpos2, 650))


pixel_x_input = IntegerInputBox('pixel_x', 'pixel_x_change', "0", 80)
pixel_x_input.set_xy((xpos1, 695))

pixel_y_input = IntegerInputBox('pixel_y', 'pixel_y_change', "0", 80)
pixel_y_input.set_xy((xpos2, 695))
