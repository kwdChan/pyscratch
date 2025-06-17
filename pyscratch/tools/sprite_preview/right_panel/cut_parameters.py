from .input_box import NumberInputBox
import pyscratch as pysc
from settings import *

row_input = NumberInputBox('n_row')
row_input.set_xy((900, 650))

col_input = NumberInputBox('n_col')
col_input.set_xy((1200, 650))
