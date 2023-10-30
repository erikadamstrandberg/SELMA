#%%

from pathlib import Path
mask_folder    = Path(__file__).parents[0]
project_folder = Path(__file__).parents[1]
shapes_folder = str(Path(project_folder,'shapes'))
gdstk_setup_folder = str(Path(project_folder,'gdstk_setup'))

import os
import sys
if shapes_folder not in sys.path:
    sys.path.append(shapes_folder)
    
if gdstk_setup_folder not in sys.path:
    sys.path.append(gdstk_setup_folder)
    
import numpy as np
import gdstk

from generic_shapes import create_annulus, create_circle, create_rectangle
from vcsel_chip_shapes import create_initial_a_mark, create_EBL_combo_mark
from initialize_layer_data import create_layer_data
from manage_gdstk import setup_gds_lib, save_gds_file, create_folder_for_mask, save_ordering_mask


def create_chip_necessities(chip_mask):
    ###### CREATE CHIP LAYOUT ######
    chip_center_x = 0
    chip_center_y = 0
    
    chip_size_x = 8000
    chip_size_y = 10000

    # Create chip
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
    
    x_offset_MS_alignment_mesa = 2750
    y_offset_MS_alignment_mesa = 3250
    
    MS_alignment_mesa_top_left = create_initial_a_mark('MS_align', -x_offset_MS_alignment_mesa, y_offset_MS_alignment_mesa,
                                                        False, 0,
                                                        chip_mask.layer_data, left_side=True)
    
    chip_mask.add_polygon_list('MS_align', MS_alignment_mesa_top_left)
    
    MS_alignment_mesa_top_right = create_initial_a_mark('MS_align', x_offset_MS_alignment_mesa, y_offset_MS_alignment_mesa,
                                                        False, 0,
                                                        chip_mask.layer_data, left_side=True)
    
    chip_mask.add_polygon_list('MS_align', MS_alignment_mesa_top_right)
    
    MS_alignment_mesa_bottom_left = create_initial_a_mark('MS_align', -x_offset_MS_alignment_mesa, -y_offset_MS_alignment_mesa,
                                                        False, 0,
                                                        chip_mask.layer_data, left_side=True)
    
    chip_mask.add_polygon_list('MS_align', MS_alignment_mesa_bottom_left)
    
    MS_alignment_mesa_bottom_right = create_initial_a_mark('MS_align', x_offset_MS_alignment_mesa, -y_offset_MS_alignment_mesa,
                                                        False, 0,
                                                        chip_mask.layer_data, left_side=True)
    
    chip_mask.add_polygon_list('MS_align', MS_alignment_mesa_bottom_right)
    
    
    x_offset_combo_mark = 2000
    y_offset_combo_mark = 3500
    
    x_offset_2_combo_mark = 900
    
    combo_mark_top_left = create_EBL_combo_mark('MS_align', -x_offset_combo_mark, y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_top_left)
    
    combo_mark_top_left2 = create_EBL_combo_mark('MS_align', -x_offset_2_combo_mark, y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_top_left2)
    
    combo_mark_top_right = create_EBL_combo_mark('MS_align', x_offset_combo_mark, y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_top_right)
    
    combo_mark_top_right2 = create_EBL_combo_mark('MS_align', x_offset_2_combo_mark, y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_top_right2)
    
    combo_mark_bottom_left = create_EBL_combo_mark('MS_align', -x_offset_combo_mark, -y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_bottom_left)
    
    combo_mark_bottom_left2 = create_EBL_combo_mark('MS_align', -x_offset_2_combo_mark, -y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_bottom_left2)
    
    combo_mark_bottom_right = create_EBL_combo_mark('MS_align', x_offset_combo_mark, -y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_bottom_right)
    
    combo_mark_bottom_right2 = create_EBL_combo_mark('MS_align', x_offset_2_combo_mark, -y_offset_combo_mark, chip_mask.layer_data)
    chip_mask.add_polygon_list('MS_align', combo_mark_bottom_right2)
    
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
    left_circles_x = -2100
    left_circles_y = 50
    chip_mask.create_TLM_circles('p_ring', left_circles_x, left_circles_y)
    
    
    lower_circles_x = -400
    lower_circles_y = -3300
    chip_mask.create_TLM_circles('p_ring', lower_circles_x, lower_circles_y)
    
    # n-circles
    left_circles_x = 1595
    left_circles_y = 50
    chip_mask.create_TLM_circles('n_ring', left_circles_x, left_circles_y)
    
    lower_circles_x = -400
    lower_circles_y = -3800
    chip_mask.create_TLM_circles('n_ring', lower_circles_x, lower_circles_y)
    
    # TLM rectangle pads
    # p-pads
    pads_right_x = 1000
    pads_right_y = 50
    chip_mask.create_TLM_pads('p_ring', -pads_right_x, pads_right_y)
    
    pads_lower_x = -200
    pads_lower_y = -3100
    chip_mask.create_TLM_pads('p_ring', pads_lower_x, pads_lower_y)
    
    # n-pads
    pads_left_x = 925
    pads_left_y = 50
    chip_mask.create_TLM_pads('n_ring', pads_left_x, pads_left_y)
   
    pads_lower_x = -200
    pads_lower_y = -3600
    chip_mask.create_TLM_pads('n_ring', pads_lower_x, pads_lower_y)


    # Add labels
    label_x = 230
    label_y = -chip_size_y/2 + 1920
    label_distance_y = 90
    
    chip_mask.create_all_labels(label_x, label_y, label_distance_y)
    
    return (chip_size_x, chip_size_y, frame_size_x, frame_size_y)

def VCSEL_y_trenches(x_offset, y_offset, mesa_radius, mesa_to_trench, chip_mask, layer_data):
    
    ## FIRST LAYER: P RING
    p_ring_x = x_offset
    p_ring_y = y_offset
    
    p_ring_outer = mesa_radius - 2.0
    p_ring_inner = p_ring_outer - 4.5
    
    chip_mask.create_annulus('p_ring', p_ring_x, p_ring_y,
                             p_ring_inner, p_ring_outer)
    
    ## SECONDS LAYER: MESA PROTECTION
    meas_x      = x_offset
    meas_y      = y_offset
    
    chip_mask.create_circle('mesa', meas_x, meas_y, mesa_radius)
    
    ## THRID LAYER: OPEN SIDEWALLS FOR OXIDATION
    sidewall_inner  = mesa_radius - 4
    sidewall_outer  = mesa_radius + 5.5
    
    sidewall_x = x_offset
    sidewall_y = y_offset
    
    chip_mask.create_annulus('open_sidewalls', sidewall_x, sidewall_y,
                             sidewall_inner, sidewall_outer)
    
    ## FIFTH LAYER: N CONTACTS
    # n_contact_thickness = 55
    distance_from_side_opening = 15
    
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
    n_contact.fillet(10000, tolerance=0.001)

    
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
    open_n_arch.fillet(10000, tolerance=0.001)
    chip_mask.add_polygon('open_contacts', open_n_arch)
    
    ## CREATE CIRCLE FOR P CONTACT
    open_p_ring_margin   = 1.5
    open_p_contat_radius = p_ring_outer - open_p_ring_margin
    
    chip_mask.create_circle('open_contacts', open_contacts_x, open_contacts_y,
                        open_p_contat_radius)
    
    ## SEVENTH LAYER: CONTACT PADS
    contact_pad_side = 70
    contact_pad_x_offset = -50 + x_offset
    contact_pad_y_offset = -100 + y_offset
    
    probe_pitch = 100
    contact_pad_radius = 35
    
    left_contact_pad = create_circle('contact_pads', contact_pad_x_offset, contact_pad_y_offset, contact_pad_radius, layer_data, chip_mask.circle_tolerance)
    right_contact_pad = create_circle('contact_pads', contact_pad_x_offset + probe_pitch, contact_pad_y_offset, contact_pad_radius, layer_data, chip_mask.circle_tolerance)

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
    
    final_angle_triangle  = 10
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
                                ( contact_pad_side/2 + contact_pad_x_offset - 10,  contact_pad_side/2 + contact_pad_y_offset - 35),
                                (-contact_pad_side/2 + contact_pad_x_offset + 9,  contact_pad_side/2 + contact_pad_y_offset - 35)],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    left_full_n_contact = gdstk.boolean(left_contact_pad, contact_pad_arch, 'or')
    left_full_n_contact = gdstk.boolean(left_full_n_contact, taper_left, 'or', layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
    
    left_full_n_contact[0].fillet(100, tolerance=0.001)
    
    chip_mask.add_polygon_list('contact_pads', left_full_n_contact)
    
    taper_right = gdstk.Polygon([(x_offset - 6, y_offset -1),
                                (x_offset + 6, y_offset -1),
                                (x_offset + 7, y_offset- 20),
                                (contact_pad_side/2 + contact_pad_x_offset + probe_pitch - 20,  contact_pad_side/2 + contact_pad_y_offset - 35),
                                (-contact_pad_side/2 + contact_pad_x_offset + probe_pitch,  contact_pad_side/2 + contact_pad_y_offset - 35)],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    cutout_radius = p_ring_inner + 1.5
    cutout_taper_right = create_circle('contact_pads', meas_x, meas_y, cutout_radius, layer_data, chip_mask.circle_tolerance)
    
    taper_right = gdstk.boolean(taper_right, cutout_taper_right, 'not',
                            layer=layer_data['contact_pads']['layer_number'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    taper_right = taper_right[0]
    
    
    right_full_n_contact = gdstk.boolean(right_contact_pad, taper_right, 'or', layer=layer_data['contact_pads']['layer_number'],
    datatype=layer_data['contact_pads']['datatype'])
    right_full_n_contact[0].fillet(100, tolerance=0.001)
    
    chip_mask.add_polygon_list('contact_pads', right_full_n_contact)
    
    
    
    ## EIGHT LAYER
    bond_pad_margin = 3
    bond_pad_radius = contact_pad_radius - bond_pad_margin
    chip_mask.create_circle('bond_pads', contact_pad_x_offset + probe_pitch, contact_pad_y_offset, bond_pad_radius)
    chip_mask.create_circle('bond_pads', contact_pad_x_offset, contact_pad_y_offset, bond_pad_radius)
    
    
    ## NINTH LAYER
    ms_align_side = 20
    x_offset_MS_align_top_right  = x_offset - 125
    y_offset_MS_align_top_right  = y_offset + 150
    
    x_offset_MS_align_top_left = x_offset + 125
    y_offset_MS_align_top_left = y_offset + 150
    
    x_offset_MS_align_bottom_right  = x_offset - 125
    y_offset_MS_align_bottom_right  = y_offset - 150
    
    x_offset_MS_align_bottom_left = x_offset + 125
    y_offset_MS_align_bottom_left = y_offset - 150
    
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_top_right, y_offset_MS_align_top_right, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_top_left, y_offset_MS_align_top_left, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_bottom_right, y_offset_MS_align_bottom_right, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_bottom_left, y_offset_MS_align_bottom_left, ms_align_side, ms_align_side)
    
    
    ## TRENCHES
    trench_width = 2
    trench_height = 25
    
    x_offset_trenches = mesa_radius + mesa_to_trench + trench_width/2
    
    chip_mask.create_rectangle('trenches', x_offset + x_offset_trenches, y_offset, trench_width, trench_height)
    chip_mask.create_rectangle('trenches', x_offset - x_offset_trenches, y_offset, trench_width, trench_height)
    
def VCSEL_x_trenches(x_offset, y_offset, mesa_radius, mesa_to_trench, chip_mask, layer_data):
    
    ## FIRST LAYER: P RING
    p_ring_x = x_offset
    p_ring_y = y_offset
    
    p_ring_outer = mesa_radius - 2.0
    p_ring_inner = p_ring_outer - 4.5
    
    chip_mask.create_annulus('p_ring', p_ring_x, p_ring_y,
                             p_ring_inner, p_ring_outer)
    
    ## SECONDS LAYER: MESA PROTECTION
    meas_x      = x_offset
    meas_y      = y_offset
    
    chip_mask.create_circle('mesa', meas_x, meas_y, mesa_radius)
    
    ## THRID LAYER: OPEN SIDEWALLS FOR OXIDATION
    sidewall_inner  = mesa_radius - 4
    sidewall_outer  = mesa_radius + 5.5
    
    sidewall_x = x_offset
    sidewall_y = y_offset
    
    chip_mask.create_annulus('open_sidewalls', sidewall_x, sidewall_y,
                             sidewall_inner, sidewall_outer)
    
    ## FIFTH LAYER: N CONTACTS
    # n_contact_thickness = 55
    distance_from_side_opening = 15
    
    n_contact_inner  = sidewall_outer + distance_from_side_opening
    n_contact_outer  = 80 #n_contact_inner + n_contact_thickness
    
    n_contact_x      = x_offset
    n_contact_y      = y_offset
    
    # CREATE ARCH
    n_contact = create_annulus('n_ring', n_contact_x, n_contact_y,
                               n_contact_inner, n_contact_outer,
                               layer_data, chip_mask.circle_tolerance)
    
    # REMOVE TRIANGLE PART: BOOLEAN 'NOT'
    initial_angle_triangle = -15
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
    n_contact.fillet(10000, tolerance=0.001)

    
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
    open_n_arch.fillet(10000, tolerance=0.001)
    chip_mask.add_polygon('open_contacts', open_n_arch)
    
    ## CREATE CIRCLE FOR P CONTACT
    open_p_ring_margin   = 1.5
    open_p_contat_radius = p_ring_outer - open_p_ring_margin
    
    chip_mask.create_circle('open_contacts', open_contacts_x, open_contacts_y,
                        open_p_contat_radius)
    
    ## SEVENTH LAYER: CONTACT PADS
    contact_pad_side = 70
    contact_pad_x_offset = -50 + x_offset
    contact_pad_y_offset = -100 + y_offset
    
    probe_pitch = 100
    contact_pad_radius = 35
    
    left_contact_pad = create_circle('contact_pads', contact_pad_x_offset, contact_pad_y_offset, contact_pad_radius, layer_data, chip_mask.circle_tolerance)
    right_contact_pad = create_circle('contact_pads', contact_pad_x_offset + probe_pitch, contact_pad_y_offset, contact_pad_radius, layer_data, chip_mask.circle_tolerance)

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
                                         (x_offset + 200 - 110, y_offset + 40),
                                         (x_offset, -10 + y_offset + 7)],
                                          layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, remove_right_margin, 'not',
                                      layer=layer_data['contact_pads']['layer_number'],
                                      datatype=layer_data['contact_pads']['datatype'])
    initial_angle_triangle = 0
    initial_angle_triangle_rad = initial_angle_triangle*np.pi/180
    
    final_angle_triangle  = 15
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
                                ( contact_pad_side/2 + contact_pad_x_offset - 10,  contact_pad_side/2 + contact_pad_y_offset - 35),
                                (-contact_pad_side/2 + contact_pad_x_offset + 9,  contact_pad_side/2 + contact_pad_y_offset - 35)],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    left_full_n_contact = gdstk.boolean(left_contact_pad, contact_pad_arch, 'or')
    left_full_n_contact = gdstk.boolean(left_full_n_contact, taper_left, 'or', layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
    
    left_full_n_contact[0].fillet(100, tolerance=0.001)
    
    chip_mask.add_polygon_list('contact_pads', left_full_n_contact)
    
    
    
    taper_right_1 = gdstk.Polygon([(x_offset+4 , y_offset+4),
                                (x_offset+4, y_offset-4),
                                (x_offset+25 , y_offset-4),
                                (x_offset+25, y_offset-100),
                                (x_offset+85 , y_offset-100),
                                (x_offset+35, y_offset+4),],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])


    
    cutout_radius = p_ring_inner + 1.5
    cutout_taper_right = create_circle('contact_pads', meas_x, meas_y, cutout_radius, layer_data, chip_mask.circle_tolerance)
    
    taper_right = gdstk.boolean(taper_right_1, cutout_taper_right, 'not',
                            layer=layer_data['contact_pads']['layer_number'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    taper_right = taper_right[0]
    
    
    right_full_n_contact = gdstk.boolean(right_contact_pad, taper_right, 'or', layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
    right_full_n_contact = right_full_n_contact[0]
    right_full_n_contact.fillet(10, tolerance=0.001)
    
    
    chip_mask.add_polygon('contact_pads', right_full_n_contact)

    
    
    
    ## EIGHT LAYER
    bond_pad_margin = 3
    bond_pad_radius = contact_pad_radius - bond_pad_margin
    chip_mask.create_circle('bond_pads', contact_pad_x_offset + probe_pitch, contact_pad_y_offset, bond_pad_radius)
    chip_mask.create_circle('bond_pads', contact_pad_x_offset, contact_pad_y_offset, bond_pad_radius)
    
    
    ## NINTH LAYER
    ms_align_side = 20
    x_offset_MS_align_top_right  = x_offset - 125
    y_offset_MS_align_top_right  = y_offset + 150
    
    x_offset_MS_align_top_left = x_offset + 125
    y_offset_MS_align_top_left = y_offset + 150
    
    x_offset_MS_align_bottom_right  = x_offset - 125
    y_offset_MS_align_bottom_right  = y_offset - 150
    
    x_offset_MS_align_bottom_left = x_offset + 125
    y_offset_MS_align_bottom_left = y_offset - 150
    
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_top_right, y_offset_MS_align_top_right, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_top_left, y_offset_MS_align_top_left, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_bottom_right, y_offset_MS_align_bottom_right, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_bottom_left, y_offset_MS_align_bottom_left, ms_align_side, ms_align_side)
    
    
    ## TRENCHES
    
    trench_width = 25
    trench_height = 2
    
    y_offset_trenches = mesa_radius + mesa_to_trench + trench_height/2
    
    chip_mask.create_rectangle('trenches', x_offset, y_offset + y_offset_trenches, trench_width, trench_height)
    chip_mask.create_rectangle('trenches', x_offset, y_offset - y_offset_trenches, trench_width, trench_height)

def VCSEL_no_trenches(x_offset, y_offset, mesa_radius, chip_mask, layer_data, grating=False):
    
    ## FIRST LAYER: P RING
    p_ring_x = x_offset
    p_ring_y = y_offset
    
    p_ring_outer = mesa_radius - 2.0
    p_ring_inner = p_ring_outer - 4.5
    
    chip_mask.create_annulus('p_ring', p_ring_x, p_ring_y,
                             p_ring_inner, p_ring_outer)
    
    ## SECONDS LAYER: MESA PROTECTION
    meas_x      = x_offset
    meas_y      = y_offset
    
    chip_mask.create_circle('mesa', meas_x, meas_y, mesa_radius)
    
    ## THRID LAYER: OPEN SIDEWALLS FOR OXIDATION
    sidewall_inner  = mesa_radius - 4
    sidewall_outer  = mesa_radius + 5.5
    
    sidewall_x = x_offset
    sidewall_y = y_offset
    
    chip_mask.create_annulus('open_sidewalls', sidewall_x, sidewall_y,
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
    n_contact.fillet(10000, tolerance=0.001)

    
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
    open_n_arch.fillet(10000, tolerance=0.001)
    chip_mask.add_polygon('open_contacts', open_n_arch)
    
    ## CREATE CIRCLE FOR P CONTACT
    open_p_ring_margin   = 1.5
    open_p_contat_radius = p_ring_outer - open_p_ring_margin
    
    chip_mask.create_circle('open_contacts', open_contacts_x, open_contacts_y,
                        open_p_contat_radius)
    
    ## SEVENTH LAYER: CONTACT PADS
    contact_pad_side = 70
    contact_pad_x_offset = -50 + x_offset
    contact_pad_y_offset = -100 + y_offset
    
    probe_pitch = 100
    contact_pad_radius = 35
    
    left_contact_pad = create_circle('contact_pads', contact_pad_x_offset, contact_pad_y_offset, contact_pad_radius, layer_data, chip_mask.circle_tolerance)
    right_contact_pad = create_circle('contact_pads', contact_pad_x_offset + probe_pitch, contact_pad_y_offset, contact_pad_radius, layer_data, chip_mask.circle_tolerance)

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
    
    final_angle_triangle  = 10
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
                                ( contact_pad_side/2 + contact_pad_x_offset - 10,  contact_pad_side/2 + contact_pad_y_offset - 35),
                                (-contact_pad_side/2 + contact_pad_x_offset + 9,  contact_pad_side/2 + contact_pad_y_offset - 35)],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    left_full_n_contact = gdstk.boolean(left_contact_pad, contact_pad_arch, 'or')
    left_full_n_contact = gdstk.boolean(left_full_n_contact, taper_left, 'or', layer=layer_data['contact_pads']['layer_number'], datatype=layer_data['contact_pads']['datatype'])
    
    left_full_n_contact[0].fillet(100, tolerance=0.001)
    
    chip_mask.add_polygon_list('contact_pads', left_full_n_contact)
    
    taper_right = gdstk.Polygon([(x_offset, y_offset),
                                (x_offset + 10, y_offset),
                                (contact_pad_side/2 + contact_pad_x_offset + probe_pitch - 7,  contact_pad_side/2 + contact_pad_y_offset - 35),
                                (-contact_pad_side/2 + contact_pad_x_offset + probe_pitch + 7,  contact_pad_side/2 + contact_pad_y_offset - 35)],
                                  layer=layer_data['contact_pads']['layer_number'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    cutout_radius = p_ring_inner + 1.5
    cutout_taper_right = create_circle('contact_pads', meas_x, meas_y, cutout_radius, layer_data, chip_mask.circle_tolerance)
    
    taper_right = gdstk.boolean(taper_right, cutout_taper_right, 'not',
                            layer=layer_data['contact_pads']['layer_number'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    taper_right = taper_right[0]
    
    
    right_full_n_contact = gdstk.boolean(right_contact_pad, taper_right, 'or', layer=layer_data['contact_pads']['layer_number'],
    datatype=layer_data['contact_pads']['datatype'])
    right_full_n_contact[0].fillet(100, tolerance=0.001)
    
    chip_mask.add_polygon_list('contact_pads', right_full_n_contact)
    
    
    
    ## EIGHT LAYER
    bond_pad_margin = 3
    bond_pad_radius = contact_pad_radius - bond_pad_margin
    chip_mask.create_circle('bond_pads', contact_pad_x_offset + probe_pitch, contact_pad_y_offset, bond_pad_radius)
    chip_mask.create_circle('bond_pads', contact_pad_x_offset, contact_pad_y_offset, bond_pad_radius)
    
    
    ## NINTH LAYER
    ms_align_side = 20
    x_offset_MS_align_top_right  = x_offset - 125
    y_offset_MS_align_top_right  = y_offset + 150
    
    x_offset_MS_align_top_left = x_offset + 125
    y_offset_MS_align_top_left = y_offset + 150
    
    x_offset_MS_align_bottom_right  = x_offset - 125
    y_offset_MS_align_bottom_right  = y_offset - 150
    
    x_offset_MS_align_bottom_left = x_offset + 125
    y_offset_MS_align_bottom_left = y_offset - 150
    
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_top_right, y_offset_MS_align_top_right, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_top_left, y_offset_MS_align_top_left, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_bottom_right, y_offset_MS_align_bottom_right, ms_align_side, ms_align_side)
    chip_mask.create_rectangle('MS_align', x_offset_MS_align_bottom_left, y_offset_MS_align_bottom_left, ms_align_side, ms_align_side)


    if grating:
        duty_cycle =  grating.get('duty_cycle')
        period = grating.get('period')
        orientation = grating.get('orientation')
        
        grating_height = 2*p_ring_inner
        grating_width  = period*duty_cycle
        
        grating_polygons = []
        
        grating_margin = 0
        grating_radius = p_ring_inner - grating_margin
        grating_outline = create_circle('pol_grating', meas_x, meas_y, grating_radius, layer_data, chip_mask.circle_tolerance)

        grating_polygons.append(grating_outline)
        
        
        max_iteration_check = 2000
        
        if orientation == 'x':
            for i in range(max_iteration_check):
                grating_line = create_rectangle('pol_grating', meas_x, meas_y + i*period, grating_height, grating_width, layer_data)
                grating_polygons = gdstk.boolean(grating_polygons, grating_line, 'not',
                                        layer=layer_data['pol_grating']['layer_number'],
                                        datatype=layer_data['pol_grating']['datatype'])
                if i*period > p_ring_inner:
                    break
                
            for i in range(max_iteration_check):
                grating_line = create_rectangle('pol_grating', meas_x, meas_y - i*period, grating_height, grating_width, layer_data)
    
                grating_polygons = gdstk.boolean(grating_polygons, grating_line, 'not',
                                        layer=layer_data['pol_grating']['layer_number'],
                                        datatype=layer_data['pol_grating']['datatype'])
                if i*period > p_ring_inner:
                    break
                
        if orientation == 'y':
            for i in range(max_iteration_check):
                grating_line = create_rectangle('pol_grating', meas_x + i*period, meas_y, grating_width, grating_height, layer_data)
                grating_polygons = gdstk.boolean(grating_polygons, grating_line, 'not',
                                        layer=layer_data['pol_grating']['layer_number'],
                                        datatype=layer_data['pol_grating']['datatype'])
                if i*period > p_ring_inner:
                    break
                
            for i in range(max_iteration_check):
                grating_line = create_rectangle('pol_grating', meas_x - i*period, meas_y, grating_width, grating_height, layer_data)
    
                grating_polygons = gdstk.boolean(grating_polygons, grating_line, 'not',
                                        layer=layer_data['pol_grating']['layer_number'],
                                        datatype=layer_data['pol_grating']['datatype'])
                if i*period > p_ring_inner:
                    break
            
        
        chip_mask.add_polygon_list('pol_grating', grating_polygons)
        
        
def main():
    # Sheet with layer definitions
    layer_definition_sheet = 'layer_definition.xlsx'
    # Create layer data and folder to 
    layer_data = create_layer_data(layer_definition_sheet, mask_folder)
    # Create folder to save mask
    create_folder_for_mask(mask_folder)

    # Mask names
    mask_name   = 'KAW_BE_WB_v1'
    # Name of top cell
    cell_name   = 'KAW_BE_WB_v1'
    
    # Setup GDS library and create all needed variables!
    chip_mask = setup_gds_lib(mask_name, cell_name, layer_data)
    
    # Create chip
    # Adds frames, alignment marks, orintation arrow, TLM structures and labels
    (chip_size_x, chip_size_y, frame_size_x, frame_size_y) = create_chip_necessities(chip_mask)


    ## VCSEL in each qudrant
    number_of_VCSEL_columns_left = 9
    number_of_VCSEL_rows_left = 9
    
    number_of_VCSEL_columns_right = 9
    number_of_VCSEL_rows_right = 9
    
    ## Offset for VCSEL qudrants
    x_offset_0_0 = -2600.0
    y_offset_0_0 = 2800.0
    
    x_offset_1_0 = 0
    y_offset_1_0 = y_offset_0_0
    
    x_offset_0_1 = x_offset_0_0
    y_offset_0_1 = -300
    
    x_offset_1_1 = x_offset_1_0
    y_offset_1_1 = y_offset_0_1
    
    x_offset_between_VCSEL = 250.0
    y_offset_between_VCSEL = 300.0
    
    
    ## Coordinates for BEAT
    x_VCSEL_positions_for_BEAT = []
    y_VCSEL_positions_for_BEAT = []
    
    x_witness_mesa_position_for_NIKON = []
    y_witness_mesa_position_for_NIKON = []
    
    
    # VCSEL_no_trenches(x_offset, y_offset, mesa_radius, chip_mask, layer_data)
    aperture_size = np.array([1.0, 1.5, 2.0, 2.0, 2.5, 2.5, 3.0, 3.5, 4.0])
    mesa_diameter = aperture_size + 19.0
    mesa_radius = mesa_diameter/2.0

    mesa_to_trench = 18
    
    ## Grating data
    grating_duty_cycle_0_0 = np.array([0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6])
    grating_duty_cycle_1_0 = np.array([0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6])
    
    grating_period = 0.26
    
    orientation_0_0 = 'x'
    orientation_1_0 = 'y'
    

    # ## 0.0 qudrant
    # for i in range(number_of_VCSEL_columns_left):
    #     for j in range(number_of_VCSEL_rows_left):
            
    #         x_pos_loop = x_offset_0_0 + x_offset_between_VCSEL*i
    #         y_pos_loop = y_offset_0_0 - y_offset_between_VCSEL*j
            
    #         grating_0_0 = {'duty_cycle': grating_duty_cycle_0_0[i],
    #                        'period': grating_period,
    #                        'orientation': orientation_0_0}
            
    #         VCSEL_no_trenches(x_pos_loop, y_pos_loop, mesa_radius[j], chip_mask, layer_data, grating=grating_0_0)
    #         x_VCSEL_positions_for_BEAT.append(x_pos_loop)
    #         y_VCSEL_positions_for_BEAT.append(y_pos_loop)
            
            
    # ## 1.0 qudrant
    # for i in range(number_of_VCSEL_columns_right):
    #     for j in range(number_of_VCSEL_rows_right):
            
    #         x_pos_loop = x_offset_1_0 + x_offset_between_VCSEL*i
    #         y_pos_loop = y_offset_1_0 - y_offset_between_VCSEL*j
            
    #         grating_1_0 = {'duty_cycle': grating_duty_cycle_1_0[i],
    #                        'period': grating_period,
    #                        'orientation': orientation_1_0}
            
    #         VCSEL_no_trenches(x_pos_loop, y_pos_loop, mesa_radius[j], chip_mask, layer_data, grating=grating_1_0)
    #         x_VCSEL_positions_for_BEAT.append(x_pos_loop)
    #         y_VCSEL_positions_for_BEAT.append(y_pos_loop)
            
            
    # mesa_to_trench = np.array([1, 2, 3, 4, 5, 6, 8, 10, 12])

    # ## 0.1 qudrant
    # for i in range(number_of_VCSEL_columns_left):
    #     for j in range(number_of_VCSEL_rows_left):
            
    #         x_pos_loop = x_offset_0_1 + x_offset_between_VCSEL*i
    #         y_pos_loop = y_offset_0_1 - y_offset_between_VCSEL*j
            
    #         VCSEL_y_trenches(x_pos_loop, y_pos_loop, mesa_radius[j], mesa_to_trench[i], chip_mask, layer_data)
            
    #         x_VCSEL_positions_for_BEAT.append(x_pos_loop)
    #         y_VCSEL_positions_for_BEAT.append(y_pos_loop)
            
            
    # ## 1.1 qudrant
    # for i in range(number_of_VCSEL_columns_right):
    #     for j in range(number_of_VCSEL_rows_right):
            
    #         x_pos_loop = x_offset_1_1 + x_offset_between_VCSEL*i
    #         y_pos_loop = y_offset_1_1 - y_offset_between_VCSEL*j
            
    #         VCSEL_x_trenches(x_pos_loop, y_pos_loop, mesa_radius[j], mesa_to_trench[i], chip_mask, layer_data)
                 
    #         x_VCSEL_positions_for_BEAT.append(x_pos_loop)
    #         y_VCSEL_positions_for_BEAT.append(y_pos_loop)
            
            
    y_offset_open_witness_mesa = 20
    width_open_witness_mesa = 80
    height_open_witness_mesa = 140
    
    x_offset_label = 25
    y_offset_label = 30
    label_text_size = 50
    
    point_size = 25
    x_offset_point = 50
    y_offset_point = 5
    
    witness_mesa_margin = 4

    ## 0.0 witness mesa
    for j in range(number_of_VCSEL_rows_left):
        if mesa_diameter[j].is_integer():
            chip_mask.create_label('mesa', x_offset_0_0 - x_offset_between_VCSEL - x_offset_label, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
        else:
            chip_mask.create_label('mesa', x_offset_0_0 - x_offset_between_VCSEL - x_offset_label, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
            chip_mask.create_label('mesa', x_offset_0_0 - x_offset_between_VCSEL - x_offset_label + x_offset_point, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label + y_offset_point, point_size, '.')
     
        chip_mask.create_circle('mesa', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_0 - y_offset_between_VCSEL*j, mesa_radius[j])
        chip_mask.create_rectangle('open_sidewalls', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa, height_open_witness_mesa)
        chip_mask.create_rectangle('witness_mesa', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        chip_mask.create_rectangle('open_contacts', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        
    ## 1/2.0 witness mesa
    for j in range(number_of_VCSEL_rows_right):
        if mesa_diameter[j].is_integer():
            chip_mask.create_label('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75 - x_offset_label, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
        else:
            chip_mask.create_label('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75 - x_offset_label, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
            chip_mask.create_label('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75 - x_offset_label + x_offset_point, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label + y_offset_point, point_size, '.')
                   
        chip_mask.create_circle('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_0 - y_offset_between_VCSEL*j, mesa_radius[j])
        chip_mask.create_rectangle('open_sidewalls', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa, height_open_witness_mesa)
        chip_mask.create_rectangle('witness_mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        chip_mask.create_rectangle('open_contacts', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
    
    ## 1.0 witness mesa
    for j in range(number_of_VCSEL_rows_right):
        if mesa_diameter[j].is_integer():
            chip_mask.create_label('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right - x_offset_label, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
        else:
            chip_mask.create_label('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right- x_offset_label, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
            chip_mask.create_label('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right- x_offset_label + x_offset_point, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_label + y_offset_point, point_size, '.')
  
        chip_mask.create_circle('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_0 - y_offset_between_VCSEL*j, mesa_radius[j])
        chip_mask.create_rectangle('open_sidewalls', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa, height_open_witness_mesa)
        chip_mask.create_rectangle('witness_mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        chip_mask.create_rectangle('open_contacts', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_0 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
   
    
    ## 0.0 witness mesa
    for j in range(number_of_VCSEL_rows_left):
        if mesa_diameter[j].is_integer():
            chip_mask.create_label('mesa', x_offset_0_0 - x_offset_between_VCSEL - x_offset_label, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
        else:
            chip_mask.create_label('mesa', x_offset_0_0 - x_offset_between_VCSEL - x_offset_label, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
            chip_mask.create_label('mesa', x_offset_0_0 - x_offset_between_VCSEL - x_offset_label + x_offset_point, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label + y_offset_point, point_size, '.')
 
        chip_mask.create_circle('mesa', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_1 - y_offset_between_VCSEL*j, mesa_radius[j])
        chip_mask.create_rectangle('open_sidewalls', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa, height_open_witness_mesa)
        chip_mask.create_rectangle('witness_mesa', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        chip_mask.create_rectangle('open_contacts', x_offset_0_0 - x_offset_between_VCSEL, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        
    ## 1/2.0 witness mesa
    for j in range(number_of_VCSEL_rows_right):
        if mesa_diameter[j].is_integer():
            chip_mask.create_label('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75 - x_offset_label, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
        else:
            chip_mask.create_label('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75 - x_offset_label, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
            chip_mask.create_label('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75 - x_offset_label + x_offset_point, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label + y_offset_point, point_size, '.')
    
        chip_mask.create_circle('mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_1 - y_offset_between_VCSEL*j, mesa_radius[j])
        chip_mask.create_rectangle('open_sidewalls', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa, height_open_witness_mesa)
        chip_mask.create_rectangle('witness_mesa', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        chip_mask.create_rectangle('open_contacts', x_offset_1_0 - x_offset_between_VCSEL*1.5 + 75, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
    
    ## 1.0 witness mesa
    for j in range(number_of_VCSEL_rows_right):
        if mesa_diameter[j].is_integer():
            chip_mask.create_label('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right - x_offset_label, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
        else:
            chip_mask.create_label('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right- x_offset_label, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label, label_text_size, str(round(mesa_diameter[j])))
            chip_mask.create_label('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right- x_offset_label + x_offset_point, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_label + y_offset_point, point_size, '.')
 
        chip_mask.create_circle('mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_1 - y_offset_between_VCSEL*j, mesa_radius[j])
        chip_mask.create_rectangle('open_sidewalls', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa, height_open_witness_mesa)
        chip_mask.create_rectangle('witness_mesa', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)
        chip_mask.create_rectangle('open_contacts', x_offset_1_0 + x_offset_between_VCSEL*number_of_VCSEL_columns_right, y_offset_0_1 - y_offset_between_VCSEL*j + y_offset_open_witness_mesa, width_open_witness_mesa - witness_mesa_margin, height_open_witness_mesa - witness_mesa_margin)




    ## IN-SITU OXIDATION STRUCTURE
    oxidation_mesa_diameter = np.arange(20, 30.5, 0.5)
    aperture_diameter = oxidation_mesa_diameter - 19
    oxidation_mesa_radius = oxidation_mesa_diameter/2
    p_ring_outer_oxidation = oxidation_mesa_radius - 2.0
    p_ring_inner_oxidation = p_ring_outer_oxidation - 4.5
    
    x_offset_oxidation = -750
    y_offset_oxidation = 75
    
    oxidation_distance = 50
    
    x_offset_oxidation_label = -25
    y_offset_oxidation_label = -80
    
    
    x_offset_rectangle_oxidation = 500
    y_offset_rectangle_oxidation = -5
    width_oxidation = 1200
    height_oxidation = 200
    
    
    show_label = np.array([20, 25, 30])
    for i in range(len(oxidation_mesa_diameter)):
        chip_mask.create_circle('mesa', x_offset_oxidation + i*oxidation_distance, y_offset_oxidation, oxidation_mesa_radius[i])
        if oxidation_mesa_diameter[i] in show_label:
            if oxidation_mesa_diameter[i] == 30:
                chip_mask.create_label('mesa', x_offset_oxidation + i*oxidation_distance + x_offset_oxidation_label, y_offset_oxidation + y_offset_oxidation_label + 100, label_text_size, str(round(aperture_diameter[i])))
            else:
                chip_mask.create_label('mesa', x_offset_oxidation + i*oxidation_distance + x_offset_oxidation_label + 12, y_offset_oxidation + y_offset_oxidation_label + 100, label_text_size, str(round(aperture_diameter[i])))
            
            
            chip_mask.create_label('mesa', x_offset_oxidation + i*oxidation_distance + x_offset_oxidation_label, y_offset_oxidation + y_offset_oxidation_label, label_text_size, str(round(oxidation_mesa_diameter[i])))

    chip_mask.create_rectangle('open_sidewalls', x_offset_oxidation + x_offset_rectangle_oxidation, y_offset_oxidation + y_offset_rectangle_oxidation, width_oxidation, height_oxidation)
    chip_mask.create_rectangle('witness_mesa', x_offset_oxidation + x_offset_rectangle_oxidation, y_offset_oxidation + y_offset_rectangle_oxidation, width_oxidation - witness_mesa_margin, height_oxidation - witness_mesa_margin)
    chip_mask.create_rectangle('open_contacts', x_offset_oxidation + x_offset_rectangle_oxidation, y_offset_oxidation + y_offset_rectangle_oxidation, width_oxidation - witness_mesa_margin, height_oxidation - witness_mesa_margin)

    

    x_offset_alignment_VCSEL = x_offset_1_0 + x_offset_between_VCSEL*(number_of_VCSEL_columns_right + 2)
    y_offset_alignment_VCSEL_0_0 = y_offset_0_0
    y_offset_alignment_VCSEL_0_1 = y_offset_0_1
    
    y_offset_between_alignment_VCSEL = y_offset_between_VCSEL

    aperture_size_alignment_VCSEL = 2.0
    mesa_diameter_alignment_VCSEL = aperture_size_alignment_VCSEL + 19.0
    mesa_radius_alignment_VCSEL = mesa_diameter_alignment_VCSEL/2.0
    
    number_of_alignment_VCSELs = number_of_VCSEL_rows_right
    
    alignment_vcsel_x = np.zeros(number_of_alignment_VCSELs*2)
    alignment_vcsel_y = np.zeros(number_of_alignment_VCSELs*2)
    
    ## Alignment VCSELs
    for j in range(number_of_alignment_VCSELs):
            VCSEL_no_trenches(x_offset_alignment_VCSEL, y_offset_alignment_VCSEL_0_0 - y_offset_between_alignment_VCSEL*j, mesa_radius_alignment_VCSEL, chip_mask, layer_data)
            alignment_vcsel_x[j] = x_offset_alignment_VCSEL
            alignment_vcsel_y[j] = y_offset_alignment_VCSEL_0_0 - y_offset_between_alignment_VCSEL*j
            
    for j in range(number_of_alignment_VCSELs):
            VCSEL_no_trenches(x_offset_alignment_VCSEL, y_offset_alignment_VCSEL_0_1 - y_offset_between_alignment_VCSEL*j, mesa_radius_alignment_VCSEL, chip_mask, layer_data)
            alignment_vcsel_x[number_of_alignment_VCSELs + j] = x_offset_alignment_VCSEL
            alignment_vcsel_y[number_of_alignment_VCSELs + j] = y_offset_alignment_VCSEL_0_1 - y_offset_between_alignment_VCSEL*j
        
        
    ## Add LI for grating etch
    LI_grating_x = 600
    LI_grating_y = 3300
    
    LI_grating_width = 500
    LI_grating_height = 500
    
    chip_mask.create_rectangle('pol_grating', LI_grating_x, LI_grating_y, LI_grating_width, LI_grating_height)
        
    ## Save coordinates for all VCSELs for nikon
    coordinates_folder =  str(mask_folder) + '\\coordinates\\'
    if not os.path.exists(coordinates_folder):
        os.makedirs(coordinates_folder)
     

    np.savetxt(coordinates_folder + 'x_VCSEL_positions_for_BEAT.csv', x_VCSEL_positions_for_BEAT, delimiter=',')
    np.savetxt(coordinates_folder + 'y_VCSEL_positions_for_BEAT.csv', y_VCSEL_positions_for_BEAT, delimiter=',')
    np.savetxt(coordinates_folder + 'alignment_vcsel_x.csv', alignment_vcsel_x, delimiter=',')
    np.savetxt(coordinates_folder + 'alignment_vcsel_y.csv', alignment_vcsel_y, delimiter=',')
    
    
    # MS_polygon = chip_mask.mask_dict['MS_align']
    
    # for polygon in MS_polygon:
    #     if isinstance(polygon, gdstk.Polygon):
    #         polygon.mirror((0,10000),(0,-10000))
    
    


    # Save .gds-file
    save_layout = True
    save_gds_file(chip_mask, mask_name, mask_folder, save_layout)
    
    mask_spacing_x             = 8000.0
    mask_spacing_y             = -10000.0
    number_of_mask_columns     = 4
        
    save_mask_for_ordering = False
    if save_mask_for_ordering:
        save_ordering_mask(chip_mask, mask_name, cell_name, mask_folder, 
                           layer_data, 
                           mask_spacing_x, mask_spacing_y, number_of_mask_columns)

if  __name__ == '__main__':
    main()
