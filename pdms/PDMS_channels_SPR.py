#%%

from pathlib import Path
import os

import numpy as np
import matplotlib.pyplot as plt

import gdstk
import re
from datetime import datetime

def create_rectangle(x, y, x_size, y_size, layer):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer)

def create_circle(key, x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius,
                        layer=layer_data[key]['layer'],
                        datatype=layer_data[key]['datatype'],
                        tolerance=tolerance
                        )


project_folder = Path(__file__).parents[0]

#%% Read channels
GDS_folder = 'GDS'
channel_mask = '10-16_10.18_SPR_Sensor_v7.3_only_channels.gds'
channel_mask_path = Path(project_folder, GDS_folder)
channel_mask_path = Path(channel_mask_path, channel_mask)
channel_lib = gdstk.read_gds(str(channel_mask_path))
channel_cells = channel_lib.cells
channel_1 = channel_cells[3].polygons[0]
# channel_top = channel_cells[0].polygons[1]

# Set units and precision for layout
unit = 1.0e-9
precision = 1.0e-10
circle_tolerance = 0.005

## LAYER DATA
wafer_layer = 1
channels_layer = 2

layer_data = {
    'wafer': {'layer': wafer_layer, 'datatype': 1},
    'channels': {'layer': channels_layer, 'datatype': 1}
}

folder_name = 'PDMS_channels_SPR'
cell_name = 'PDMS_channels_SPR_v3_4inch'
mask_name = cell_name
save_layout = True

mask_folder = Path(project_folder, folder_name)
if not os.path.exists(mask_folder):
    os.makedirs(mask_folder)

# Set units and precision for layout
unit = 1.0e-6
precision = 1.0e-10
circle_tolerance = 0.005


## CREATE THE MASK ##
# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
gdstk.Library()

# Main cell of mask
mask = lib.new_cell(cell_name)

two_inch = 4*2.54e-2
two_inch_um = two_inch*1e6
inverted_mask = create_circle('wafer', 0, 0, two_inch_um/2, layer_data, circle_tolerance)

                        # inverted_mask = gdstk.boolean(inverted_mask, polygon_and_cells_copy, 'not')
                        
                        

inverted_mask = gdstk.boolean(inverted_mask, channel_1.copy(), 'not')
# inverted_mask = gdstk.boolean(inverted_mask, channel_top.copy(), 'not')


# second_set_x = -first_set_x
# second_set_y = first_set_y
# left_channel = channel_polygons.copy().translate(second_set_x - offset_channels_x/2, second_set_y)
# inverted_mask = gdstk.boolean(inverted_mask, left_channel, 'not')
# right_channel = channel_polygons.copy().translate(second_set_x + offset_channels_x/2, second_set_y)
# inverted_mask = gdstk.boolean(inverted_mask, right_channel, 'not')

# third_set_x = -first_set_x
# third_set_y = -first_set_y
# left_channel = channel_polygons.copy().translate(third_set_x - offset_channels_x/2, third_set_y)
# inverted_mask = gdstk.boolean(inverted_mask, left_channel, 'not')
# right_channel = channel_polygons.copy().translate(third_set_x + offset_channels_x/2, third_set_y)
# inverted_mask = gdstk.boolean(inverted_mask, right_channel, 'not')

# foruth_set_x = first_set_x
# foruth_set_y = -first_set_y
# left_channel = channel_polygons.copy().translate(foruth_set_x - offset_channels_x/2, foruth_set_y)
# inverted_mask = gdstk.boolean(inverted_mask, left_channel, 'not')
# right_channel = channel_polygons.copy().translate(foruth_set_x + offset_channels_x/2, foruth_set_y)
# inverted_mask = gdstk.boolean(inverted_mask, right_channel, 'not')


for polygon in inverted_mask:
    mask.add(polygon)
        

save_path = Path(mask_folder, cell_name)
lib.write_gds(str(save_path) + '.gds')
    

