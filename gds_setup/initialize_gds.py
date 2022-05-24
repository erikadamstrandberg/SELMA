#%%

import gdstk
import os

def setup_gds_lib(mask_name, cell_name, layer_data):
    # Set units and precision for layout
    unit      = 1.0e-6
    precision = 1.0e-10
    circle_tolerance = 0.005
    
    ## CREATE THE MASK ##
    # The GDSII file is called a library, which contains multiple cells.
    lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
    gdstk.Library()
    
    # Main cell of mask
    mask = lib.new_cell(cell_name)
    
    layer_data_reversed = {}    
    for k, v in layer_data.items():
        layer_data_reversed[v['layer_number']] = k
        
    full_mask = {}
    
    for layer in layer_data.keys():
        full_mask[layer] = lib.new_cell(layer)
        
    return (mask, full_mask, layer_data_reversed, lib, circle_tolerance)
    
def save_gds_file(full_mask, mask_folder, mask, mask_name, lib, save_layout):
    created_mask_folder =  str(mask_folder) + '\\mask\\'
    
    ### Add cell to main layer
    for layer in full_mask.keys():
        if type(full_mask[layer]) == gdstk.Polygon:
            # print(type(full_mask[layer]) == gdstk.Polygon)
            cell_layer = gdstk.Reference(full_mask[layer])
            mask.add(cell_layer)
        
    # Save the library in a file called 'first.gds'.
    # if save_layout:
    #     lib.write_gds(created_mask_folder + mask_name + '.gds')
        
def create_folder_for_mask(mask_folder):
    created_mask_folder =  str(mask_folder) + '\\mask\\'
        
    if not os.path.exists(created_mask_folder):
        os.makedirs(created_mask_folder)