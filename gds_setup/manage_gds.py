#%%

import gdstk
import os
import sys
from pathlib import Path

project_folder = Path(__file__).parents[1]
mask_creation_folder = str(Path(project_folder,'mask_creation'))

if mask_creation_folder not in sys.path:
    sys.path.append(mask_creation_folder)
    
from generic_shapes import create_rectangle
from vcsel_chip_shapes import create_a_marks_top, create_a_marks_all_layers, create_orientation_arrow, create_TLM_circles, TLM_pads, create_all_labels



class full_mask:
    
    
    def __init__(self, mask_dict, mask_cell, layer_data, layer_data_reversed, gds_lib,  circle_tolerance):
        self.mask_dict = mask_dict
        self.mask_cell = mask_cell
        self.layer_data = layer_data
        self.layer_data_reversed = layer_data_reversed
        self.gds_lib = gds_lib
        self.circle_tolerance = circle_tolerance
        
    def create_rectangle(key, x, y, x_size, y_size, rotation=0):
        
        self.mask_dict[key] = create_rectangle(key, x, y, x_size, y_size, rotation=rotation)
        

def setup_gds_lib(mask_name, cell_name, layer_data):
    # Set units and precision for layout
    unit      = 1.0e-6
    precision = 1.0e-10
    circle_tolerance = 0.005
    
    ## CREATE THE MASK ##
    # The GDSII file is called a library, which contains multiple cells.
    gds_lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
    gdstk.Library()
    
    # Main cell of mask
    mask_cell = gds_lib.new_cell(cell_name)
    
    layer_data_reversed = {}    
    for k, v in layer_data.items():
        layer_data_reversed[v['layer_number']] = k
        
    mask_dict = {}
    
    for layer in layer_data.keys():
        mask_dict[layer] = [gds_lib.new_cell(layer)]
        
    return full_mask(mask_dict, mask_cell, layer_data, layer_data_reversed, gds_lib,  circle_tolerance)
    



def save_gds_file(chip_mask, mask_name, mask_folder, save_layout):
    created_mask_folder =  str(mask_folder) + '\\mask\\'
    
    ### Add cell to main layer
    for layer in chip_mask.mask_dict.keys():
        # print(full_mask[layer])
        for cells in chip_mask.mask_dict[layer]:
            if type(cells) == gdstk.Polygon:
            # print(polygon)
            # print(type(full_mask[layer]) == gdstk.Polygon)
            # cell_layer = gdstk.Reference(full_mask[layer])
            # print(gdstk.Reference(full_mask[layer]))
                chip_mask.mask_cell.add(cells)
        
    # Save the library in a file called 'first.gds'.
    if save_layout:
        chip_mask.gds_lib.write_gds(created_mask_folder + mask_name + '.gds')
        
def create_folder_for_mask(mask_folder):
    created_mask_folder =  str(mask_folder) + '\\mask\\'
        
    if not os.path.exists(created_mask_folder):
        os.makedirs(created_mask_folder)