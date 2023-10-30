#%%

from pathlib import Path
import os

import numpy as np
import matplotlib.pyplot as plt

import gdstk
import re
from datetime import datetime

def create_circle(key, x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius, 
                        layer=layer_data[key]['layer'],
                        datatype=layer_data[key]['datatype'],
                        tolerance=tolerance
                        )

def create_rectangle(key, x, y, x_size, y_size, layer_data, rotation=0):
    
    right_x = x + x_size/2
    left_x  = x - x_size/2
    
    upper_y = y + y_size/2
    lower_y = y - y_size/2
    
    polygon = gdstk.Polygon([(right_x, upper_y),
                             (right_x, lower_y),
                             (left_x,  lower_y),
                             (left_x,  upper_y)],
                            layer=layer_data[key]['layer'],
                            datatype=layer_data[key]['datatype']).rotate(rotation)
    
    return polygon


project_folder = Path(__file__).parents[0]

#%% Read channels
GDS_folder = 'GDS'
contact_mask_path = Path(project_folder, GDS_folder)
contact_mask = 'KAW_BE_v2_contact_layer.gds'
contact_mask_path = Path(contact_mask_path, contact_mask)
contact_lib = gdstk.read_gds(str(contact_mask_path))
contact_cells = contact_lib.cells

# Set units and precision for layout
unit = 1.0e-9
precision = 1.0e-10
circle_tolerance = 0.005

## LAYER DATA
traces_layer = 1

layer_data = {
    'traces': {'layer': traces_layer, 'datatype': 1}
}

folder_name = 'trace_masks'
cell_name = 'test_traces'
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

x_slide_center = 0
y_slide_center = 0
x_slide_size = 26000
y_slide_size = 76000
inverted_mask = create_rectangle('traces', x_slide_center, y_slide_center, x_slide_size, y_slide_size, layer_data)

polygons_for_inverted_mask = []
                
bond_pad_size = 100
x = 0
y = 2000

x_size_trace = 180
y_size_trace = 10000

number_of_traces_x = 20
delta_x = 320
for i in range(-int(number_of_traces_x/2), int(number_of_traces_x/2) + 1):
    trace_bond_pad = create_circle('traces', x + i*delta_x, y, bond_pad_size, layer_data, circle_tolerance)        
    polygons_for_inverted_mask.append(trace_bond_pad)
    
    trace = create_rectangle('traces', x + i*delta_x, y-y_size_trace/2, x_size_trace, y_size_trace, layer_data, rotation=0)
    polygons_for_inverted_mask.append(trace)
    
    trace_bond_pad = create_circle('traces', x + i*delta_x, y-y_size_trace, bond_pad_size, layer_data, circle_tolerance)        
    polygons_for_inverted_mask.append(trace_bond_pad)
    

x = -4500
y = 3000

number_of_traces_y = 20 
delta_y = 320

x_size_trace_small = 50
y_size_trace_small = 180
x_extra = 320

for i in range(number_of_traces_y):
    
    trace_bond_pad = create_circle('traces', x, y + i*delta_y, bond_pad_size, layer_data, circle_tolerance)        
    polygons_for_inverted_mask.append(trace_bond_pad)
    
    x_size_trace_small = x_size_trace_small + x_extra
    
    trace = create_rectangle('traces', x - x_size_trace_small/2, y + i*delta_y, x_size_trace_small, y_size_trace_small, layer_data, rotation=0)
    polygons_for_inverted_mask.append(trace)
    
    trace = create_rectangle('traces', x - x_size_trace_small, y-y_size_trace/2 + x_size_trace/2 + delta_y*i , x_size_trace, y_size_trace, layer_data, rotation=0)
    polygons_for_inverted_mask.append(trace)
    
    trace_bond_pad = create_circle('traces', x - x_size_trace_small, y-y_size_trace + x_size_trace/2 + delta_y*i, bond_pad_size, layer_data, circle_tolerance)        
    polygons_for_inverted_mask.append(trace_bond_pad)
    
x = 4500
y = 3000

number_of_traces_y = 20 
delta_y = 320

x_size_trace_small = 50
y_size_trace_small = 180
x_extra = 320

for i in range(number_of_traces_y):
    
    trace_bond_pad = create_circle('traces', x, y + i*delta_y, bond_pad_size, layer_data, circle_tolerance)        
    polygons_for_inverted_mask.append(trace_bond_pad)
    
    x_size_trace_small = x_size_trace_small + x_extra
    
    trace = create_rectangle('traces', x + x_size_trace_small/2, y + i*delta_y, x_size_trace_small, y_size_trace_small, layer_data, rotation=0)
    polygons_for_inverted_mask.append(trace)
    
    trace = create_rectangle('traces', x + x_size_trace_small, y-y_size_trace/2 + x_size_trace/2 + delta_y*i , x_size_trace, y_size_trace, layer_data, rotation=0)
    polygons_for_inverted_mask.append(trace)
    
    trace_bond_pad = create_circle('traces', x + x_size_trace_small, y-y_size_trace + x_size_trace/2 + delta_y*i, bond_pad_size, layer_data, circle_tolerance)        
    polygons_for_inverted_mask.append(trace_bond_pad)
    
    
for polygon in polygons_for_inverted_mask:
    inverted_mask = gdstk.boolean(inverted_mask, polygon, 'not')
    
mask.add(inverted_mask[0])

save_path = Path(mask_folder, mask_name)
lib.write_gds(str(save_path) + '.gds')
    

