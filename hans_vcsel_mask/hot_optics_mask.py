#%%
import os 

from pathlib import Path
mask_folder    = Path(__file__).parents[0]
project_folder = Path(__file__).parents[1]
shapes_folder = str(Path(project_folder,'shapes'))
gdstk_setup_folder = str(Path(project_folder,'gdstk_setup'))

import sys
if shapes_folder not in sys.path:
    sys.path.append(shapes_folder)
    
if gdstk_setup_folder not in sys.path:
    sys.path.append(gdstk_setup_folder)
    
from generic_shapes import create_rectangle
from initialize_layer_data import create_layer_data
from manage_gdstk import setup_gds_lib, save_gds_file, create_folder_for_mask

import gdstk

def create_chip_necessities(chip_mask):
    ###### CREATE CHIP LAYOUT ######
    chip_center_x = 0
    chip_center_y = 0
    
    chip_size_x = 8000
    chip_size_y = 10000

    # Create chip'
    chip_mask.create_rectangle('chip', chip_center_x, chip_center_y, chip_size_x, chip_size_y)
    
    # Create DF, CF frame
    frame_marginal_x = 2000
    frame_marginal_y = 2000
    frame_size_x = chip_size_x - frame_marginal_x
    frame_size_y = chip_size_y - frame_marginal_y
    
    chip_mask.create_rectangle('DD_frame', chip_center_x, chip_center_y, frame_size_x, frame_size_y)
    chip_mask.create_rectangle('DC_frame', chip_center_x, chip_center_y, frame_size_x, frame_size_y)
    
    # Alignment marks
    colums_of_alignment_marks = 4
    aligment_mark_squares     = 500
    chip_mask.create_initial_a_marks_all_layers(frame_size_x, frame_size_y, colums_of_alignment_marks)
    chip_mask.create_a_marks_all_layers(chip_size_x, chip_size_y, frame_size_x, frame_size_y, colums_of_alignment_marks, aligment_mark_squares)
    
    # Orientation arrow
    arrow_head          = 400
    arrow_base          = 500
    arrow_margin        = 50
    orientation_arrow_x = 0
    orientation_arrow_y = frame_size_y/2 - arrow_head - arrow_margin
    
    chip_mask.create_orientation_arrow('p_ring', orientation_arrow_x, orientation_arrow_y,
                                       arrow_head, arrow_base)
    
    # TLM circle pads
    # p-circles
    left_circles_x = -1875
    left_circles_y = 50
    chip_mask.create_TLM_circles('p_ring', left_circles_x, left_circles_y)
    
    
    lower_circles_x = -400
    lower_circles_y = -3300
    chip_mask.create_TLM_circles('p_ring', lower_circles_x, lower_circles_y)
    
    # n-circles
    left_circles_x = 1875
    left_circles_y = 50
    chip_mask.create_TLM_circles('n_ring', left_circles_x, left_circles_y)
    
    lower_circles_x = -400
    lower_circles_y = -3800
    chip_mask.create_TLM_circles('n_ring', lower_circles_x, lower_circles_y)
    
    # TLM rectangle pads
    # p-pads
    pads_right_x = 665
    pads_right_y = 50
    chip_mask.create_TLM_pads('p_ring', -pads_right_x, pads_right_y)
    
    pads_lower_x = -200
    pads_lower_y = -3100
    chip_mask.create_TLM_pads('p_ring', pads_lower_x, pads_lower_y)
    
    # n-pads
    pads_left_x = 1100
    pads_left_y = 50
    chip_mask.create_TLM_pads('n_ring', pads_left_x, pads_left_y)
   
    pads_lower_x = -200
    pads_lower_y = -3600
    chip_mask.create_TLM_pads('n_ring', pads_lower_x, pads_lower_y)


    # Add labels
    label_x = 230
    label_y = -chip_size_y/2 + 1920
    label_distance_y = 60
    
    chip_mask.create_all_labels(label_x, label_y, label_distance_y)
    
    return (chip_size_x, chip_size_y, frame_size_x, frame_size_y)
    
        
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
    
    # Create chip
    # Adds frames, alignment marks, orintation arrow, TLM structures and labels
    (chip_size_x, chip_size_y, frame_size_x, frame_size_y) = create_chip_necessities(chip_mask)


    ######### ADD CODE HERE #########
    #### Create function for VCSEL ####
    #### Create function for witness mesas ####
    #### Loop over all of it ####
    
    
    #### Example for creation of elements ####
    #### PLEASE REMOVE ####
    x = 0
    y = 0
    x_size = 100
    y_size = 200
    chip_mask.create_rectangle('p_ring', x, y, x_size, y_size)
    
    
    #### Using booleans ####
    x = 0
    y = -400
    square = create_rectangle('p_ring', x, y, x_size, y_size, layer_data)
    cutout = create_rectangle('p_ring', x, y, x_size/2, y_size/2, layer_data)

    square_with_hole = gdstk.boolean(square, cutout, 'not')
    
    #### Add a list to chip mask ####
    chip_mask.add_polygon_list('p_ring', square_with_hole)
        
    
        
    #### Create circle ####
    x = 400
    y = 0
    radius = 300
    chip_mask.create_circle('mesa', x, y, radius)
    
    #### Create annulus ####
    x = -400
    y = 0
    inner_radius = 300
    outer_radius = 100
    chip_mask.create_annulus('n_ring', x, y, inner_radius, outer_radius)
    
    
    #### Crete text ####
    x = 0
    y = 500
    size = 500
    chip_mask.create_label('contact_pads', x, y, size, 'Hans')
    
    
    
    
    
    
    
    
    
    
    # Save .gds-file
    save_layout = True
    save_gds_file(chip_mask, mask_name, mask_folder, save_layout)




if  __name__ == '__main__':
    main()
