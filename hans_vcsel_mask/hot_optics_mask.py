#%%
import os 
import warnings

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
    
from generic_shapes import create_rectangle, create_circle, create_half_annulus, create_rotated_rectangle, create_polygon
from initialize_layer_data import create_layer_data
from manage_gdstk import setup_gds_lib, save_gds_file, create_folder_for_mask

import gdstk
import numpy as np

#%% 

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

def deg2rad(deg):
    return deg/180*np.pi
    
        
def main():
    
    # Sheet with layer definitions
    layer_definition_sheet = 'layer_definition_v2.xlsx'
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

    # Create VCSEL coordinate arrays.
    # x_start:      x-coordinate of the edge most VCSEL column
    # x_step:       step size in x direction
    # x_centre:     x-coordinate of the centre most VCSEL column
    
    # y_start:      y-coordinate of the edge most VCSEL row
    # y_step:       step size in y direction
    # y_centre:     y-coordinate of the centre most VCSEL row
    
    x_edge = 2655
    x_step = 390
    x_centre = 315
        
    y_edge = 2800
    y_step = 355
    y_centre = 315
    
    if (x_edge-x_centre)%x_step != 0:
        warnings.warn("VCSEL x-coordinate start, stop and step mismatching.")
    
    if (y_edge-y_centre)%y_step != 0:
        warnings.warn("VCSEL y-coordinate start, stop and step mismatching.")
        
    # Create two different halvesfor x coordinates.
    x_neg = np.linspace(-x_edge,-x_centre,(x_edge-x_centre)//x_step+1)
    x_pos = np.linspace(x_centre,x_edge,(x_edge-x_centre)//x_step+1)
    # Concatenate the two arrays
    x_coordinates = np.append(x_neg,x_pos)
    
    # Create two different halvesfor y coordinates.
    y_neg = np.linspace(-y_edge,-y_centre,(y_edge-y_centre)//y_step+1)
    y_pos = np.linspace(y_centre,y_edge,(y_edge-y_centre)//y_step+1)
    # Concatenate the two arrays
    y_coordinates = np.append(y_neg,y_pos) 

    
    ## LAYER 1: p_ring
    p_ring_outer_d =  13
    p_ring_inner_d =  6
    
    p_ring_outer_r = p_ring_outer_d/2
    p_ring_inner_r = p_ring_inner_d/2
    
    for x in x_coordinates:
        for y in y_coordinates:
            chip_mask.create_annulus('p_ring', x, y, p_ring_inner_r, p_ring_outer_r)
            
    ## Layer 2: top mesa
    top_mesa_d = p_ring_outer_d + 1
    top_mesa_r = top_mesa_d/2
    
    for x in x_coordinates:
        for y in y_coordinates:
            chip_mask.create_circle('mesa', x, y, top_mesa_r)
            
    ## Layer 3: SiNx open
    sinx_open_inner_d = p_ring_outer_d - 3
    sinx_open_inner_r = sinx_open_inner_d/2
    
    sinx_open_outer_d = 30
    sinx_open_outer_r = sinx_open_outer_d/2
    
    for x in x_coordinates:
        for y in y_coordinates:
            chip_mask.create_annulus('open_sidewalls', x, y, sinx_open_inner_r, sinx_open_outer_r)
            
    ## Layer 4: Bottom mesa
    bottom_mesa_d = sinx_open_outer_d + 20
    bottom_mesa_r = bottom_mesa_d/2

    for x in x_coordinates:
        for y in y_coordinates:
            chip_mask.create_circle('bottom_mesa', x, y, bottom_mesa_r)
            
            
    # ## Layer 5: 
    # # TODO crate n-contact variation sweep
    # # vary inner and outer radius (y direction), also vary start and stop angle (x-direction)
    angle_stop = 6/5*np.pi
    angle_start_100 = 0
    angle_start_50 = np.pi/2
    angle_start_75 = np.pi/4
    
    n_contact_inner_d =  bottom_mesa_d + 10
    n_contact_outer_d =  n_contact_inner_d + 100
    
    n_contact_inner_r =  n_contact_inner_d/2
    n_contact_outer_r_100 =   n_contact_outer_d/2
    n_contact_outer_r_50 = n_contact_outer_r_100/np.sqrt(2)
    n_contact_outer_r_75 = n_contact_outer_r_100/np.sqrt(4/3)
    
    
    angle_start_array = np.array([angle_start_100, angle_start_75, angle_start_100, angle_start_50, angle_start_50, angle_start_100, angle_start_75, angle_start_100, angle_start_50, angle_start_50, angle_start_100, angle_start_75, angle_start_100, angle_start_50, angle_start_50, angle_start_100])
    angle_stop_array =  np.array([angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop, angle_stop])
    
    n_contact_inner_r_array = np.array([n_contact_inner_r, n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r,n_contact_inner_r])
    n_contact_outer_r_array = np.array([n_contact_outer_r_100,  n_contact_outer_r_75, n_contact_outer_r_50, n_contact_outer_r_100, n_contact_outer_r_50, n_contact_outer_r_100,  n_contact_outer_r_75, n_contact_outer_r_50, n_contact_outer_r_100, n_contact_outer_r_50, n_contact_outer_r_100,  n_contact_outer_r_75, n_contact_outer_r_50, n_contact_outer_r_100, n_contact_outer_r_50, n_contact_outer_r_100])
    
    
    
    for i in range(len(x_coordinates)):
        for j in range(len(y_coordinates)):
            chip_mask.create_half_annulus('n_ring', x_coordinates[i], y_coordinates[j],n_contact_inner_r_array[j], n_contact_outer_r_array[j],angle_start_array[j], angle_stop_array[j])
 
    # ## Layer 6:
    # calculate the radial overlap in terms of 
    
    for i in range(len(x_coordinates)):
        for j in range(len(y_coordinates)):
            r_inner = n_contact_inner_r_array[j]

            # Set margins compared to previous layer
            radial_margin = 5        #um
            angular_margin_dist = 5  #um
            
            #Translate the length unit to angular unit
            angular_margin_ang = angular_margin_dist/r_inner
            
            #Set angle start and stop with margins.
            ang_start = angle_start_array[j] - angular_margin_ang
            ang_stop = angle_stop_array[j] + angular_margin_ang
            
            #Set radial start and stop with margins.
            r_start = n_contact_inner_r_array[j]
            r_stop =  n_contact_outer_r_array[j] + radial_margin
            

            
            circ = create_circle('open_contacts', x_coordinates[i], y_coordinates[j], r_start, layer_data=layer_data, tolerance = 0.005)
            half_ann = create_half_annulus('open_contacts', x_coordinates[i], y_coordinates[j], r_start-1, r_stop, ang_start, ang_stop, layer_data=layer_data, tolerance = 0.005)
            n_contact_open = gdstk.boolean(circ, half_ann, 'or', layer=layer_data['open_contacts']['layer_number'],datatype=layer_data['open_contacts']['datatype'])
            chip_mask.add_polygon_list('open_contacts', n_contact_open)
            
    ## Layer 7: BCB
    bcb_inner_r_array = n_contact_inner_r_array + 5
    bcb_outer_r_array = n_contact_outer_r_array - 2.5
    
    #Translate the length unit to angular unit
    angular_margin_dist_bcb = 3
    angular_margin_ang_bcb = angular_margin_dist_bcb/r_inner
            
    #Set angle start and stop with margins.
    angle_start_array_bcb = angle_start_array + angular_margin_ang_bcb
    angle_stop_array_bcb = angle_stop_array - angular_margin_ang_bcb
    
    #Create a big rectangle and then remove all the small features using booleans  
    bcb_frame = create_rectangle('bcb', 0, 0, 6000, 6000, layer_data=layer_data, rotation=0)
    
    #Set up chip edge dimensions (the small rectangle on ind. laser) and offset
    d_x_bcb = 310
    d_y_bcb = 275
    offset_x = 0
    offset_y = -30
    
    for i in range(len(x_coordinates)):
        for j in range(len(y_coordinates)):
           ind_rect =  create_rectangle('bcb', x_coordinates[i]+offset_x, y_coordinates[j]+offset_y, d_x_bcb, d_y_bcb, layer_data=layer_data, rotation=0)
           half_ann_bcb = create_half_annulus('bcb', x_coordinates[i], y_coordinates[j], bcb_inner_r_array[j], bcb_outer_r_array[j], angle_start_array_bcb[j], angle_stop_array_bcb[j], layer_data=layer_data, tolerance = 0.005)
           bcb_cell = gdstk.boolean(ind_rect, half_ann_bcb, 'not', layer=layer_data['bcb']['layer_number'],datatype=layer_data['bcb']['datatype'])
           bcb_frame = gdstk.boolean(bcb_frame, bcb_cell, 'not', layer=layer_data['bcb']['layer_number'],datatype=layer_data['bcb']['datatype'])

    chip_mask.add_polygon_list('bcb', bcb_frame)
    
    #Create outer frame and fill small rect under
    #small rectangle
    chip_mask.create_rectangle('bcb', 0, -3500, 2000, 1000)
    
    #outer frame
    big_rect = create_rectangle('bcb', 0, 0, 8000, 10000, layer_data=layer_data, rotation=0)
    cutout = create_rectangle('bcb', 0, 0, 6000, 8000, layer_data=layer_data, rotation=0)
    big_frame = gdstk.boolean(big_rect, cutout, 'not', layer=layer_data['bcb']['layer_number'], datatype=layer_data['bcb']['datatype'])
    chip_mask.add_polygon_list('bcb', big_frame)
    
    
    ## Layer 8: BCB contact etch
    bcb_cont_inner_r_array = bcb_inner_r_array + 2.5
    bcb_cont_outer_r_array = bcb_outer_r_array - 2.5
    
    #Translate the length unit to angular unit
    angular_margin_dist_bcb_cont = 2
    angular_margin_ang_bcb_cont_array = angular_margin_dist_bcb_cont/r_inner
            
    #Set angle start and stop with margins.
    angle_start_array_bcb_cont = angle_start_array_bcb + angular_margin_ang_bcb_cont_array
    angle_stop_array_bcb_cont = angle_stop_array_bcb - angular_margin_ang_bcb_cont_array
    
    #Create a big rectangle and then remove all the small features using booleans  
    cutout = create_rectangle('bcb_etch_cont', 0, 0, 6000, 6000, layer_data=layer_data, rotation=0)
    
    for i in range(len(x_coordinates)):
        for j in range(len(y_coordinates)):
           chip_mask.create_half_annulus('bcb_etch_cont', x_coordinates[i], y_coordinates[j],  bcb_cont_inner_r_array[j], bcb_cont_outer_r_array[j], angle_start_array_bcb_cont[j], angle_stop_array_bcb_cont[j])
           
    # Cover alignment marks of BCB layer
    x_bcb_algn = 2250
    y_bcb_algn = 3250
    
    chip_mask.create_rectangle('bcb_etch_cont', x_bcb_algn, y_bcb_algn, 500, 500)
    chip_mask.create_rectangle('bcb_etch_cont', -x_bcb_algn, y_bcb_algn, 500, 500)
    chip_mask.create_rectangle('bcb_etch_cont', x_bcb_algn, -y_bcb_algn, 500, 500)
    chip_mask.create_rectangle('bcb_etch_cont', -x_bcb_algn, -y_bcb_algn, 500, 500)
    
    # Fix other frame sections
    rect1 = create_rectangle('bcb_etch_cont', 0, 0, 6000, 6000, layer_data=layer_data, rotation=0)
    cut1 = create_rectangle('bcb_etch_cont', 0, -30, 5620, 5875, layer_data=layer_data, rotation=0)
    small_frame_bcb_cont = gdstk.boolean(rect1, cut1, 'not', layer=layer_data['bcb_etch_cont']['layer_number'], datatype=layer_data['bcb_etch_cont']['datatype'])
    chip_mask.add_polygon_list('bcb_etch_cont', small_frame_bcb_cont)
    
    rect2 = create_rectangle('bcb_etch_cont', 0, 0, 320, 6000, layer_data=layer_data, rotation=0)
    rect3 = create_rectangle('bcb_etch_cont', 0, -30, 6000, 355, layer_data=layer_data, rotation=0)
    middle_axes_bcb_cont = gdstk.boolean(rect2, rect3, 'or', layer=layer_data['bcb_etch_cont']['layer_number'], datatype=layer_data['bcb_etch_cont']['datatype'])
    chip_mask.add_polygon_list('bcb_etch_cont', middle_axes_bcb_cont)
    
    chip_mask.create_rectangle('bcb_etch_cont', -x_bcb_algn, -y_bcb_algn, 500, 500)
    chip_mask.create_rectangle('bcb_etch_cont', 0, -3500, 2000, 1000)
           
    
    # Layer 9: Sinx on BCB
    #do the half annulus
    sinx_on_bcb_half_ann_inner_r_array = bcb_cont_inner_r_array + 2
    sinx_on_bcb_half_ann_outer_r_array = bcb_cont_outer_r_array - 2
    
    #Create the cricle array
    sinx_on_cbc_circle_r = top_mesa_r - 2
    
    #Translate the length unit to angular unit for angular margins
    angular_margin_dist_sinx_on_bcb = 1.5
    angular_margin_ang_sinx_on_bcb_array = angular_margin_dist_sinx_on_bcb/sinx_on_bcb_half_ann_inner_r_array[0]
    
    #Set angle start and stop with margins.
    angle_start_array_sinx_on_bcb = angle_start_array_bcb_cont + angular_margin_ang_sinx_on_bcb_array
    angle_stop_array_sinx_on_bcb = angle_stop_array_bcb_cont - angular_margin_ang_sinx_on_bcb_array
    
    for i in range(len(x_coordinates)):
        for j in range(len(y_coordinates)):
            
            x = x_coordinates[i]
            y = y_coordinates[j]
            
            half_ann_in_r = sinx_on_bcb_half_ann_inner_r_array[j]
            half_ann_out_r = sinx_on_bcb_half_ann_outer_r_array[j]
            
            ang_start = angle_start_array_sinx_on_bcb[j]
            ang_stop = angle_stop_array_sinx_on_bcb[j]
            
        
            
            chip_mask.create_circle('sinx_bcb', x, y, sinx_on_cbc_circle_r)
            chip_mask.create_half_annulus('sinx_bcb', x, y, half_ann_in_r, half_ann_out_r, ang_start, ang_stop)
            
    # Layer 10: contact pads
    y_offset = 110 #offset from centre of vcsel to centre of bondpad
    separation = 100 #distance between centre of VCSELs
    width_contact = 75 #diameter of contacts
    
    
    #Create contact to p-side in the following order
    for x in x_coordinates:
        for y in y_coordinates:            
            #top_square = create_rectangle('contact_pads', x+separation/2, y-y_offset, width_contact, width_contact)
            #chip_mask.create_rectangle('contact_pads', x+separation/2, y-y_offset, width_contact, width_contact)
            
            #p-contact
            small_neg_circ = create_circle('contact_pads', x, y, (p_ring_outer_r + p_ring_inner_r)/2, layer_data=layer_data, tolerance = 0.005)
            angle_to_p_pad_centre = np.arctan(separation/2/y_offset)
            rect_length = n_contact_inner_r_array[j]-5
            rect_width = (p_ring_outer_r + p_ring_inner_r)
            rect_x_offset = rect_length/2*np.sin(angle_to_p_pad_centre)
            rect_y_offset = rect_length/2*np.cos(angle_to_p_pad_centre)
            rect_from_tc = create_rotated_rectangle('contact_pads', x+rect_x_offset, y-rect_y_offset, rect_width, rect_length, layer_data, angle_to_p_pad_centre)
            rect_without_circle = gdstk.boolean(rect_from_tc, small_neg_circ, 'not', layer=layer_data['contact_pads']['layer_number'],datatype=layer_data['contact_pads']['datatype'])
            chip_mask.add_polygon_list('contact_pads', rect_without_circle)
            
            #Create the coordinates for the polygon connecting the circular contact pads with the p contact rectangle
            x1 = x + (rect_width/2*np.cos(angle_to_p_pad_centre) - rect_length/2*np.sin(angle_to_p_pad_centre))
            y1 = y + (rect_width/2*np.sin(angle_to_p_pad_centre) + rect_length/2*np.cos(angle_to_p_pad_centre))
            
            x2 = x + -(rect_width/2*np.cos(angle_to_p_pad_centre) - rect_length/2*np.sin(angle_to_p_pad_centre))
            y2 = y + -(rect_width/2*np.sin(angle_to_p_pad_centre) + rect_length/2*np.cos(angle_to_p_pad_centre))
            
            x3 = x+separation/2 + width_contact/2*(1-np.sin(angle_to_p_pad_centre))
            y3 = y-y_offset + width_contact/2*np.cos(angle_to_p_pad_centre)
            
            x4 = x+separation/2 - width_contact/2*(1-np.sin(angle_to_p_pad_centre))
            y4 = y-y_offset - width_contact/2*np.cos(angle_to_p_pad_centre)
            
            polygon_1 = create_polygon('contact_pads',x1, y1, x2, y2, x3, y3, x4, y4,layer_data=layer_data)
            #chip_mask.create_polygon('contact_pads', x1, y1, x2, y2, x3, y3, x4, y4)
            chip_mask.add_polygon('contact_pads', polygon_1)
            
            #pad_circ = create_circle('contact_pads', x+separation/2, y-y_offset, width_contact/2, layer_data=layer_data, tolerance = 0.005)
            chip_mask.create_circle('contact_pads', x+separation/2, y-y_offset, width_contact/2)
            
            
            
            chip_mask.create_circle('contact_pads', x-separation/2, y-y_offset, width_contact/2)
            
            
    # Layer 11: bondpads
    

    for x in x_coordinates:
        for y in y_coordinates:            
            #top_square = create_rectangle('contact_pads', x+separation/2, y-y_offset, width_contact, width_contact)
            #chip_mask.create_rectangle('contact_pads', x+separation/2, y-y_offset, width_contact, width_contact)
            chip_mask.create_circle('bondpads', x+separation/2, y-y_offset, width_contact/2-2.5)
            chip_mask.create_circle('bondpads', x-separation/2, y-y_offset, width_contact/2-2.5)
    # Create half annuli
    
    
    #Reverse this figure that was created
    #reverse_rect = create_rectangle('bcb_etch_cont', 0, 0, 6000, 6000, layer_data=layer_data, rotation=0)
    #bcb_etch_contours = gdstk.boolean(reverse_rect, cutout, 'not', layer=layer_data['bcb_etch_cont']['layer_number'],datatype=layer_data['bcb_etch_cont']['datatype'])
    #chip_mask.add_polygon_list('bcb_etch_cont', bcb_etch_contours)
   
    
    ######### ADD CODE HERE #########
    #### Create function for VCSEL ####
    #### Create function for witness mesas ####
    #### Loop over all of it ####
    
    
    #### Example for creation of elements ####
    #### PLEASE REMOVE ####
    #x = 0
    #y = 0
    #x_size = 100
    #y_size = 200
    #chip_mask.create_rectangle('p_ring', x, y, x_size, y_size)
    
    
    #### Using booleans ####
    #x = 0
    #y = -400
    #square = create_rectangle('p_ring', x, y, x_size, y_size, layer_data)
    #cutout = create_rectangle('p_ring', x, y, x_size/2, y_size/2, layer_data)

    #square_with_hole = gdstk.boolean(square, cutout, 'not')
    
    #### Add a list to chip mask ####
    #chip_mask.add_polygon_list('p_ring', square_with_hole)
        
    
        
    #### Create circle ####
    #x = 400
    #y = 0
    #radius = 300
    #chip_mask.create_circle('mesa', x, y, radius)
    
    #### Create annulus ####
    #x = -400
    #y = 0
    #inner_radius = 300
    #outer_radius = 100
    #chip_mask.create_annulus('n_ring', x, y, inner_radius, outer_radius)
    
    
    #### Crete text ####
    #x = 0
    #y = 500
    #size = 500
    #chip_mask.create_label('contact_pads', x, y, size, 'Hans')
    
    
    
    
    
    
    
    
    
    # Save .gds-file
    save_layout = True
    save_gds_file(chip_mask, mask_name, mask_folder, save_layout)




if  __name__ == '__main__':
    main()
