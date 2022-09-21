#%%
import os 

import numpy as np

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
    
from generic_shapes import create_rectangle, create_annulus, create_circle
from initialize_layer_data import create_layer_data
from manage_gdstk import setup_gds_lib, save_gds_file, create_folder_for_mask, save_ordering_mask

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

def VCSEL(x_offset, y_offset, p_ring_inner, p_ring_outer, chip_mask, layer_data):
    
    ## FIRST LAYER: P RING
    p_ring_x = x_offset
    p_ring_y = y_offset
    
    p_ring = chip_mask.create_annulus('p_ring', p_ring_x, p_ring_y,
                                      p_ring_inner, p_ring_outer)
    
    ## SECONDS LAYER: MESA PROTECTION
    mesa_radius = p_ring_outer + 2.0
    meas_x      = x_offset
    meas_y      = y_offset
    
    mesa = chip_mask.create_circle('mesa', meas_x, meas_y, mesa_radius)
    
    ## THRID LAYER: OPEN SIDEWALLS FOR OXIDATION
    sidewall_inner  = mesa_radius - 4
    sidewall_outer  = mesa_radius + 5.5
    
    sidewall_x = x_offset
    sidewall_y = y_offset
    
    sidewall = chip_mask.create_annulus('open_sidewalls', sidewall_x, sidewall_y,
                                        sidewall_inner, sidewall_outer)
    
    ## FIFTH LAYER: N CONTACTS
    # n_contact_thickness = 55
    distance_from_side_opening = 5
    
    n_contact_inner  = sidewall_outer + distance_from_side_opening
    n_contact_outer  = 80 #n_contact_inner + n_contact_thickness
    
    n_contact_x      = x_offset
    n_contact_y      = y_offset
    
    # CREATE ARCH
    n_contact = create_annulus('n_ring', n_contact_x, n_contact_y,
                               n_contact_inner, n_contact_outer,
                               layer_data, chip_mask.circle_tolerance)
    
    # REMOVE TRIANGLE PART: BOOLEAN 'NOT'
    initial_angle_triangle = 0
    initial_angle_triangle_rad = initial_angle_triangle*np.pi/180
    
    final_angle_triangle  = 40
    final_angle_triangle_rad = final_angle_triangle*np.pi/180
    
    triangle_end_x = n_contact_outer + 500
    
    triangle_initial_end_y = triangle_end_x*np.tan(initial_angle_triangle_rad)
    triangle_final_end_y   = triangle_end_x*np.tan(final_angle_triangle_rad)
    
    triangle = gdstk.Polygon([(n_contact_x, n_contact_y),
                              (triangle_end_x + x_offset, -triangle_initial_end_y + y_offset),
                              (-triangle_end_x + x_offset, -triangle_final_end_y + y_offset)])
    
    n_contact = gdstk.boolean(n_contact, triangle, 'not',
                            layer=layer_data['n_ring']['layer_number'],
                            datatype=layer_data['n_ring']['datatype'])
    
    ## REMOVE SQUARE: BOOLEAN 'NOT'
    square_x_offset = -60 + x_offset
    square_y_offset = -120 + y_offset
    square_side = 70
    square = gdstk.Polygon([(-square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset,  square_side + square_y_offset),
                            (-square_side + square_x_offset,  square_side + square_y_offset)])
    
    n_contact = gdstk.boolean(n_contact, square, 'not',
                              layer=layer_data['n_ring']['layer_number'],
                              datatype=layer_data['n_ring']['datatype'])
    n_contact = n_contact[0]
    
    chip_mask.add_polygon('n_ring', n_contact)

    ## SIXTH LAYER: OPEN CONTACTS
    ## CREATE ARCH FOR N CONTACTS
    ## THE SAME SETUP AS THE CONTACTS
    ## CREATE ANNULUS, REMOVE TRIANGLE AND SQUARE
    open_contact_margin = 2
        
    open_contacts_x = x_offset
    open_contacts_y = y_offset
    
    open_contacts_inner = n_contact_inner + open_contact_margin
    open_contacts_outer = n_contact_outer - open_contact_margin
    
    open_contact_arch = create_annulus('n_ring', open_contacts_x, open_contacts_y,
                        open_contacts_inner, open_contacts_outer,
                        layer_data, chip_mask.circle_tolerance)

    
    # REMOVE TRIANGLE PART: BOOLEAN 'NOT'
    triangle_x_offset = 2 
    triangle_y_offset = open_contact_margin
    
    triangle = gdstk.Polygon([(n_contact_x - triangle_x_offset, n_contact_y + triangle_y_offset),
                              (triangle_end_x - triangle_x_offset + x_offset, -triangle_initial_end_y + triangle_y_offset + y_offset),
                              (-triangle_end_x - triangle_x_offset + x_offset, -triangle_final_end_y + triangle_y_offset + y_offset)])
    
    open_n_arch = gdstk.boolean(open_contact_arch, triangle, 'not', 
                            layer=layer_data['open_contacts']['layer_number'], 
                            datatype=layer_data['open_contacts']['datatype'])
    ## REMOVE SQUARE: BOOLEAN 'NOT'
    square_x_offset = square_x_offset
    square_y_offset = square_y_offset + open_contact_margin
    
    
    square = gdstk.Polygon([(-square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset,  square_side + square_y_offset),
                            (-square_side + square_x_offset,  square_side + square_y_offset)])
    
    open_n_arch = gdstk.boolean(open_n_arch, square, 'not',
                           layer=layer_data['open_contacts']['layer_number'],
                           datatype=layer_data['open_contacts']['datatype'])
    
    open_n_arch = open_n_arch[0]
    chip_mask.add_polygon('open_contacts', open_n_arch)
    
    ## CREATE CIRCLE FOR P CONTACT
    open_p_ring_margin   = 1.5
    open_p_contat_radius = p_ring_outer - open_p_ring_margin
    
    open_p_contact = chip_mask.create_circle('open_contacts', open_contacts_x, open_contacts_y,
                        open_p_contat_radius)
    
    ## SEVENTH LAYER: CONTACT PADS
    contact_pad_side = 70
    contact_pad_x_offset = -50 + x_offset
    contact_pad_y_offset = -100 + y_offset
    
    probe_length = 100
    
    contact_pad_left = gdstk.Polygon([(-contact_pad_side/2 + contact_pad_x_offset, -contact_pad_side/2 + contact_pad_y_offset),
                                      ( contact_pad_side/2 + contact_pad_x_offset, -contact_pad_side/2 + contact_pad_y_offset),
                                      ( contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset),
                                      (-contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset)],
                                        layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
      
    chip_mask.add_polygon('contact_pads', contact_pad_left)

    
    
    contact_pad_right = gdstk.Polygon([(-contact_pad_side/2 + contact_pad_x_offset + probe_length, -contact_pad_side/2 + contact_pad_y_offset),
                                        ( contact_pad_side/2 + contact_pad_x_offset + probe_length, -contact_pad_side/2 + contact_pad_y_offset),
                                        ( contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset),
                                        (-contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset)],
                                        layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
    
    chip_mask.add_polygon('contact_pads', contact_pad_right)
    
    contact_pad_arch_inner  = n_contact_inner
    contact_pad_arch_outer  = n_contact_outer + 5
    
    contact_pad_x      = x_offset
    contact_pad_y      = y_offset
    
    contact_pad_arch = create_annulus('contact_pads', contact_pad_x, contact_pad_y,
                               contact_pad_arch_inner, contact_pad_arch_outer,
                               layer_data, chip_mask.circle_tolerance)

    remove_arch_radius = contact_pad_arch_outer - 40
    
    remove_arch = create_circle('contact_pads', contact_pad_x, contact_pad_y,
                                remove_arch_radius, 
                                layer_data, chip_mask.circle_tolerance)
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, remove_arch, 'not',
                                     layer=layer_data['contact_pads']['layer_number'],
                                     datatype=layer_data['contact_pads']['datatype'])
    
    remove_right_margin = gdstk.Polygon([(x_offset, 2*open_contact_margin + y_offset),
                                         (x_offset + 200, 2*open_contact_margin + y_offset),
                                         (x_offset + 200, -10 + y_offset),
                                         (x_offset, -10 + y_offset)],
                                          layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, remove_right_margin, 'not',
                                     layer=layer_data['contact_pads']['layer_number'],
                                     datatype=layer_data['contact_pads']['datatype'])
    initial_angle_triangle = 0
    initial_angle_triangle_rad = initial_angle_triangle*np.pi/180
    
    final_angle_triangle  = 40
    final_angle_triangle_rad = final_angle_triangle*np.pi/180
    
    triangle_end_x = n_contact_outer + 500
    
    triangle_initial_end_y = triangle_end_x*np.tan(initial_angle_triangle_rad)
    triangle_final_end_y   = triangle_end_x*np.tan(final_angle_triangle_rad)
    
    
    triangle = gdstk.Polygon([(n_contact_x, n_contact_y),
                              (triangle_end_x + x_offset, -triangle_initial_end_y + y_offset),
                              (-triangle_end_x + x_offset, -triangle_final_end_y + y_offset)])

    contact_pad_arch = gdstk.boolean(contact_pad_arch, triangle, 'not',
                                     layer=layer_data['contact_pads']['layer_number'],
                                     datatype=layer_data['contact_pads']['datatype'])
    square_side = 100
    square_x_offset = -50 + x_offset
    square_y_offset = -100 + y_offset
    
    square = gdstk.Polygon([(-square_side/2 + square_x_offset, -square_side/2 + square_y_offset),
                            ( square_side/2 + square_x_offset, -square_side/2 + square_y_offset),
                            ( square_side/2 + square_x_offset,  square_side/2 + square_y_offset),
                            (-square_side/2 + square_x_offset,  square_side/2 + square_y_offset)])
    
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, square, 'not',
                            layer=layer_data['contact_pads']['layer_number'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    contact_pad_arch = contact_pad_arch[0]
    chip_mask.add_polygon('contact_pads', contact_pad_arch)
    
    points_contact_pad = contact_pad_arch.points
    contact_pad_x = points_contact_pad[:, 0]
    contact_pad_y = points_contact_pad[:, 1]

    list_x_x1 = np.array([])
    list_y_x1 = np.array([])
    
    list_x_x2 = np.array([])
    list_y_x2 = np.array([])
    for i, y in enumerate(contact_pad_y):
        if y_offset < 0 :
            if np.abs(y)+y_offset < 0.5:
                list_x_x1 = np.append(list_x_x1, contact_pad_x[i])
                list_y_x1 = np.append(list_y_x1, contact_pad_y[i])
                
        if y_offset >= 0 :
            if np.abs(y)-y_offset < 0.5:
                list_x_x1 = np.append(list_x_x1, contact_pad_x[i])
                list_y_x1 = np.append(list_y_x1, contact_pad_y[i])
                
        if y <= y_offset:
            list_x_x2 = np.append(list_x_x2, contact_pad_x[i])
            list_y_x2 = np.append(list_y_x2, contact_pad_y[i])

    x1 = np.min(list_x_x1)
    y1 = list_y_x1[np.argmin(list_x_x1)]
    
    x2 = np.max(list_x_x2)
    y2 = list_y_x2[np.argmax(list_x_x2)]
    
    taper_left = gdstk.Polygon([(x1, y1),
                                (x2, y2),
                                ( contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset),
                                (-contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset)],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    chip_mask.add_polygon('contact_pads', taper_left)
    
    taper_right = gdstk.Polygon([(x_offset, y_offset),
                                (x_offset + 10, y_offset),
                                (contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset),
                                (-contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset)],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    cutout_radius = p_ring_inner + 1.5
    cutout_taper_right = create_circle('contact_pads', meas_x, meas_y, cutout_radius, layer_data, chip_mask.circle_tolerance)
    
    taper_right = gdstk.boolean(taper_right, cutout_taper_right, 'not',
                            layer=layer_data['contact_pads']['layer_number'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    taper_right = taper_right[0]
    chip_mask.add_polygon('contact_pads', taper_right)
    
    bond_pad_margin = 3
    
    bond_pad_left = gdstk.Polygon([(-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                      ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset, -contact_pad_side/2 + bond_pad_margin+ contact_pad_y_offset),
                                      ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset),
                                      (-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset)],
                                        layer=layer_data['bond_pads']['layer_number'], datatype=layer_data['bond_pads']['datatype'])
    
    chip_mask.add_polygon('bond_pads', bond_pad_left)
    
    
    bond_pad_right = gdstk.Polygon([(-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset + probe_length, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                       ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset + probe_length, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                       ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset + probe_length,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset),
                                       (-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset + probe_length,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset)],
                                        layer=layer_data['bond_pads']['layer_number'], datatype=layer_data['bond_pads']['datatype'])
    
    chip_mask.add_polygon('bond_pads', bond_pad_right)
    
def main():
    
    save_mask_for_ordering = False
    
    # Sheet with layer definitions
    layer_definition_sheet = 'layer_definition.xlsx'
    # Create layer data and folder to 
    layer_data = create_layer_data(layer_definition_sheet, mask_folder)
    # Create folder to save mask
    create_folder_for_mask(mask_folder)

    # Mask names
    mask_name   = 'KAW_BE_v1'
    # Name of top cell
    cell_name   = 'KAW_BE_v1'
    
    # Setup GDS library and create all needed variables!
    chip_mask = setup_gds_lib(mask_name, cell_name, layer_data)
    
    # Create chip
    # Adds frames, alignment marks, orintation arrow, TLM structures and labels
    (chip_size_x, chip_size_y, frame_size_x, frame_size_y) = create_chip_necessities(chip_mask)

    x_offset = -2400
    y_offset = 2400
    
    p_ring_inner = 7.75 - 4.5
    p_ring_outer = 7.75
    
    VCSEL(x_offset  , y_offset, p_ring_inner, p_ring_outer, chip_mask, layer_data)

    # for i in range(10):
    #     for j in range(10):
    #         VCSEL(x_offset + 250*i, y_offset - 250*j, p_ring_inner, p_ring_outer, chip_mask, layer_data)
    
    
    
    # Save .gds-file
    save_layout = True
    save_gds_file(chip_mask, mask_name, mask_folder, save_layout)
    
    mask_spacing_x             = 8000
    mask_spacing_y             = -10000
    number_of_mask_columns     = 5
        
    if save_mask_for_ordering:
        save_ordering_mask(chip_mask, mask_name, cell_name, mask_folder, 
                           layer_data, 
                           mask_spacing_x, mask_spacing_y, number_of_mask_columns)

if  __name__ == '__main__':
    main()
