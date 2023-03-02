#%%

import os 

import numpy as np
import matplotlib.pyplot as plt

from scipy import constants
c     = constants.speed_of_light
mu_0  = constants.mu_0
eps_0 = constants.epsilon_0

import gdstk 
from pathlib import Path

#%%
SELMA_path = Path(__file__).parent.resolve()


def create_mask_label(x, y, text, layer_data):
    height = 10
    
    return gdstk.text(text, height,
                       (x, y),
                       layer=layer_data['layer'],
                       datatype=layer_data['datatype'])
def create_rectangle(x, y, width, height, full_mask, layer, layer_data):
    full_mask[layer].add(gdstk.rectangle((x - width/2, y - height/2), 
                                         (x + width/2, y + height/2),
                                         layer=layer_data[layer]['layer'],
                                         datatype=layer_data[layer]['datatype']))
    
def create_ruler(x, y, line_width, line_height, number_of_line, full_mask, layer, layer_data):
    
    for i in range(number_of_line):
        create_rectangle(x, y + i*line_width*2, line_height, line_width, full_mask, 'ruler', layer_data)
   
    

def main():
    ## SETUP VARIABLES ##
    
    mask_name   = 'THE_GOLDEN_RULER_v1'
    
    # Name of cell
    cell_name   = 'THE_GOLDEN_RULER_v1'
    
    save_layout = True
    
    # Set units and precision for layout
    unit      = 1.0e-6
    precision = 1.0e-10
    circle_tolerance = 0.00001
    
    ## CREATE THE MASK ##
    # The GDSII file is called a library, which contains multiple cells.
    lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
    gdstk.Library()
    
    ## MAIN CELL
    mask = lib.new_cell(cell_name)
    
    ## LAYER DATA
    ruler_layer = 2
    lables_layer = 3
    chip_layer = 1
    
    layer_data = {
        'ruler': {'layer': ruler_layer, 'datatype': 1},
        'labels': {'layer': lables_layer, 'datatype': 1},
        'chip': {'layer': chip_layer, 'datatype': 1}
    }

    ## SAVE FULL MASK IN DIC FOR EASY REFERENCING
    full_mask = {}
    for layer in layer_data.keys():
        full_mask[layer] = lib.new_cell(layer)
        
    layer_data_reversed = {}    
    for k, v in layer_data.items():
        layer_data_reversed[v['layer']] = k
        
        
    chip_x = 0
    chip_y = 0
    chip_size_x = 8000
    chip_size_y = 10000
        
    create_rectangle(chip_x, chip_y, chip_size_x, chip_size_y, full_mask, 'chip', layer_data)
    
    ruler_x = 2000
    ruler_y = 0
    line_height = 500
    line_width = 5
    number_of_line = 400
    
    create_ruler(ruler_x, ruler_y, line_width, line_height, number_of_line, full_mask, 'ruler', layer_data)
    
    ruler_x = 1000
    ruler_y = 0
    line_height = 500
    line_width = 10
    number_of_line = 200
    
    create_ruler(ruler_x, ruler_y, line_width, line_height, number_of_line, full_mask, 'ruler', layer_data)
    
    ruler_x = 0
    ruler_y = 0
    line_height = 500
    line_width = 20
    number_of_line = 100
    
    create_ruler(ruler_x, ruler_y, line_width, line_height, number_of_line, full_mask, 'ruler', layer_data)
    
    
        
        
    ## ADD ALL CREATED CELLS TO MAIN LAYER
    for layer in full_mask.keys():
        cell_layer = gdstk.Reference(full_mask[layer])
        mask.add(cell_layer)

    ## CREATE FOLDER FOR MASKS
    mask_folder = 'MASKS'
    mask_folder_path = Path.joinpath(SELMA_path, mask_folder)
    if not os.path.exists(str(mask_folder_path)):
        os.makedirs(str(mask_folder_path))
        
        
    ## SAVE THE GENERATED MASK
    if save_layout:
        gds_file_name = mask_name + '.gds'
        save_mask_path = Path.joinpath(mask_folder_path, gds_file_name)
        lib.write_gds(str(save_mask_path))
        
if  __name__ == '__main__':
    main()

        