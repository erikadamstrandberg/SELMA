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
    
from generic_shapes import create_rectangle
from vcsel_chip_shapes import create_a_marks_top, create_a_marks_all_layers, create_orientation_arrow, create_TLM_circles, TLM_pads, create_all_labels
from initialize_layer_data import create_layer_data
from manage_gds import setup_gds_lib, save_gds_file, create_folder_for_mask

import gdstk

def create_chip_necessities(circle_tolerance, layer_data, full_mask):
    ###### CREATE CHIP LAYOUT ######
    chip_center_x = 0
    chip_center_y = 0
    
    chip_size_x = 8000
    chip_size_y = 10000

    # Create chip'
    create_rectangle('chip', chip_center_x, chip_center_y, chip_size_x, chip_size_y, layer_data, full_mask)
    
    # Create DF, CF frame
    frame_marginal_x = 2000
    frame_marginal_y = 2000
    frame_size_x = chip_size_x - frame_marginal_x
    frame_size_y = chip_size_y - frame_marginal_y
    
    create_rectangle('DD_frame', chip_center_x, chip_center_y, frame_size_x, frame_size_y, layer_data, full_mask)
    create_rectangle('DC_frame', chip_center_x, chip_center_y, frame_size_x, frame_size_y, layer_data, full_mask)
    
    # Alignment marks
    colums_of_alignment_marks = 4
    create_a_marks_all_layers(frame_size_x, frame_size_y, colums_of_alignment_marks, layer_data, full_mask)
    # create_a_marks_top(frame_size_x, frame_size_y, colums_of_alignment_marks, layer_data, full_mask)
    
    # Orientation arrow
    arrow_head          = 400
    arrow_base          = 500
    arrow_margin        = 50
    orientation_arrow_x = 0
    orientation_arrow_y = frame_size_y/2 - arrow_head - arrow_margin
    
    create_orientation_arrow('p_ring', orientation_arrow_x, orientation_arrow_y,
                             arrow_head, arrow_base,
                             layer_data, full_mask)
    
    
    # TLM circle pads
    # p-circles
    left_circles_x = -1875
    left_circles_y = 50
    create_TLM_circles('p_ring', left_circles_x, left_circles_y, layer_data, full_mask, circle_tolerance)
    
    lower_circles_x = -400
    lower_circles_y = -3300
    create_TLM_circles('p_ring', lower_circles_x, lower_circles_y, layer_data, full_mask, circle_tolerance)
    
    # n-circles
    left_circles_x = 1875
    left_circles_y = 50
    create_TLM_circles('n_ring', left_circles_x, left_circles_y, layer_data, full_mask, circle_tolerance)
    
    lower_circles_x = -400
    lower_circles_y = -3800
    create_TLM_circles('n_ring', lower_circles_x, lower_circles_y, layer_data, full_mask, circle_tolerance)
    
    # TLM rectangle pads
    # p-pads
    pads_right_x = 665
    pads_right_y = 50
    TLM_pads('p_ring', -pads_right_x, pads_right_y, layer_data, full_mask)
    
    pads_lower_x = -200
    pads_lower_y = -3100
    TLM_pads('p_ring', pads_lower_x, pads_lower_y, layer_data, full_mask)
    
    # n-pads
    pads_left_x = 1100
    pads_left_y = 50
    TLM_pads('n_ring', pads_left_x, pads_left_y, layer_data, full_mask)
   
    pads_lower_x = -200
    pads_lower_y = -3600
    TLM_pads('n_ring', pads_lower_x, pads_lower_y, layer_data, full_mask)


    # Add labels
    label_x = 230
    label_y = -chip_size_y/2 + 1920
    
    create_all_labels(label_x, label_y, layer_data, full_mask)
    

        
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
    chip_mask = setup_gds_lib(mask_name, cell_name, layer_data)
    
    # create_rectangle('DD_frame', chip_center_x, chip_center_y, frame_size_x, frame_size_y, layer_data, full_mask)
    
    chip_center_x = 0
    chip_center_y = 0
    
    chip_size_x = 8000
    chip_size_y = 10000
    
    

    # Create chip'
    create_rectangle('chip', chip_center_x, chip_center_y, chip_size_x, chip_size_y, layer_data, full_mask)

    # Adds frames, alignment marks, orintation arrow, TLM structures and labels
  ##  create_chip_necessities(circle_tolerance, layer_data, full_mask)
    
    # Create VCSELs
    
    

    # Save .gds-file
    save_layout = True
    save_gds_file(chip_mask, mask_name, mask_folder, save_layout)




if  __name__ == '__main__':
    main()
