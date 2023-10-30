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
SELMA_path = Path(__file__).parent.resolve()

def create_rectangle(key, x, y, x_size, y_size, layer_data):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer_data[key]['layer'],
                         datatype=layer_data[key]['datatype'])

def create_circle(key, x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius, 
                        layer=layer_data[key]['layer'],
                        datatype=layer_data[key]['datatype'],
                        tolerance=tolerance
                        )

def create_mask_label(x, y, text, layer_data):
    height = 80
    
    return gdstk.text(text, height,
                       (x, y),
                       layer=layer_data['layer'],
                       datatype=layer_data['datatype'])

def main():
    ## SETUP VARIABLES ##
    
    mask_name   = 'POL_GRAT_LI_v1'
    
    # Name of cell
    cell_name   = 'POL_GRAT_LI_v1'
    
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
    pixalated_circles_layer = 1
    lables_layer = 2
    chip_layer = 3
    
    layer_data = {
        'pol_grating': {'layer': pixalated_circles_layer, 'datatype': 1},
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
        
        
    chip_size_x = 8000
    chip_size_y = 10000
    full_mask['chip'].add(create_rectangle('chip', 0, 0, chip_size_x, chip_size_y, layer_data))
    
    # LI_grating_x = 600
    LI_grating_x = -2700
    LI_grating_y = 3300
    LI_grating_width = 500
    LI_grating_height = 500
    
    full_mask['labels'].add(create_rectangle('labels', LI_grating_x, LI_grating_y, LI_grating_width, LI_grating_height, layer_data))
            
    
    
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

        