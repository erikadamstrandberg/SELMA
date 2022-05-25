#%%
import os 

from pathlib import Path
mask_folder    = Path(__file__).parents[0]
project_folder = Path(__file__).parents[1]
mask_creation_folder = str(Path(project_folder,'mask_creation'))
gds_setup_folder = str(Path(project_folder,'gds_setup'))

import sys
if mask_creation_folder not in sys.path:
    sys.path.append(mask_creation_folder)
    
if gds_setup_folder not in sys.path:
    sys.path.append(gds_setup_folder)
    
from generic_shapes import create_rectangle, create_annulus
from vcsel_chip_shapes import create_a_marks_all_layers, create_orientation_arrow
from initialize_layer_data import create_layer_data
from manage_gds import setup_gds_lib, save_gds_file, create_folder_for_mask

import gdstk

        
def main():
    
    # Sheet with layer definitions
    layer_definition_sheet = 'layer_definition.xlsx'
    # Create layer data and folder to 
    layer_data = create_layer_data(layer_definition_sheet, mask_folder)
    # Create folder to save mask
    create_folder_for_mask(mask_folder)

    # Mask names
    mask_name   = 'Hans_VCSEL'
    # Name of top cell
    cell_name   = 'HOT_OPTICS_VCSEL'
    
    # Setup GDS library and create all needed variables!
    (mask, full_mask, layer_data_reversed, lib, circle_tolerance) = setup_gds_lib(mask_name, cell_name, layer_data)



    ###### CREATE CHIP LAYOUT ######
    chip_center_x = 0
    chip_center_y = 0
    
    chip_size_x = 8000
    chip_size_y = 10000

    # Create chip
    create_rectangle('chip', chip_center_x, chip_center_y, chip_size_x, chip_size_y, layer_data, full_mask)
    
    # Create DF, CF frame
    frame_marginal_x = 2000
    frame_marginal_y = 2000
    frame_size_x = chip_size_x - frame_marginal_x
    frame_size_y = chip_size_y - frame_marginal_y
    
    create_rectangle('CF_frame', chip_center_x, chip_center_y, frame_size_x, frame_size_y, layer_data, full_mask)
    create_rectangle('DF_frame', chip_center_x, chip_center_y, frame_size_x, frame_size_y, layer_data, full_mask)
    
    # Alignment marks
    colums_of_alignment_marks = 4
    create_a_marks_all_layers(frame_size_x, frame_size_y, colums_of_alignment_marks, layer_data, full_mask)
    
    # Orientation arrow
    arrow_head          = 400
    arrow_base          = 500
    arrow_margin        = 50
    orientation_arrow_x = 0
    orientation_arrow_y = frame_size_y/2 - arrow_head - arrow_margin
    
    create_orientation_arrow('p_ring', orientation_arrow_x, orientation_arrow_y,
                             arrow_head, arrow_base,
                             layer_data, full_mask)
    
    
    
    # Save .gds-file
    save_layout = True
    save_gds_file(full_mask, mask_folder, mask, mask_name, lib, save_layout)




if  __name__ == '__main__':
    main()
