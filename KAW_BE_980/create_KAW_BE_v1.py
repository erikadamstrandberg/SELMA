#%%

import os 

import numpy as np
import math

from scipy import constants
c     = constants.speed_of_light
mu_0  = constants.mu_0
eps_0 = constants.epsilon_0

import gdstk

#%%

def create_annulus(x, y,
                   inner, outer,
                   layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                         outer, 
                         inner_radius=inner, 
                         initial_angle=0,
                         final_angle=2*np.pi,
                         layer=layer_data['layer'],
                         datatype=layer_data['datatype'],
                         tolerance=tolerance
                         )

def create_half_annulus(x, y,
                        inner, outer,
                        initial_angle, final_angle,
                        layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                         outer, 
                         inner_radius=inner, 
                         initial_angle=initial_angle,
                         final_angle=final_angle,
                         layer=layer_data['layer'],
                         datatype=layer_data['datatype'],
                         tolerance=tolerance
                         )

def create_circle(x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius, 
                        layer=layer_data['layer'],
                        datatype=layer_data['datatype'],
                        tolerance=tolerance
                        )

def create_rectangle(x, y, x_size, y_size, layer_data):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                           layer=layer_data['layer'],
                           datatype=layer_data['datatype'])

def create_mask_label(x, y, text, layer_data):
    height = 60
    
    return gdstk.text(text, height,
                       (x, y),
                       layer=layer_data['layer'],
                       datatype=layer_data['datatype'])

def create_mesa_label(x, y, text, layer_data):
    height = 40
    
    return gdstk.text(text, height,
                       (x, y),
                       layer=layer_data['layer'],
                       datatype=layer_data['datatype'])

def create_alignment_mark(x, y,
                          thickness, length,
                          x_offset_rectangles, y_offset_rectangles,
                          rectangle_width, rectangle_height,
                          first_y_offset, repeating_y_offset, marks_y_direction,
                          with_rectangle,
                          layer_data):
    alignment_polygons = []
    alignment_polygons.append(gdstk.Polygon([(x + thickness/2,      y + thickness/2),
                                             (x + thickness/2 + length, y + thickness/2),
                                             (x + thickness/2 + length, y - thickness/2),
                                             (x + thickness/2,          y - thickness/2),
                                             (x + thickness/2,          y - thickness/2 - length),
                                             (x - thickness/2,          y - thickness/2 - length),
                                             (x - thickness/2,          y - thickness/2),
                                             (x - thickness/2 - length, y - thickness/2),
                                             (x - thickness/2 - length, y + thickness/2),
                                             (x - thickness/2,          y + thickness/2),
                                             (x - thickness/2,          y + thickness/2 + length),
                                             (x + thickness/2,          y + thickness/2 + length)],
                                            layer=layer_data['layer'],
                                            datatype=layer_data['datatype']))
    
    if with_rectangle:
        for i in range(marks_y_direction):
            alignment_polygons.append(create_rectangle(x - x_offset_rectangles, y + first_y_offset + i*repeating_y_offset, 
                                                       rectangle_width, rectangle_height, 
                                                       layer_data))
            alignment_polygons.append(create_rectangle(x - x_offset_rectangles, y - first_y_offset - i*repeating_y_offset, 
                                                       rectangle_width, rectangle_height, 
                                                       layer_data))
            
        for i in range(marks_y_direction):
            alignment_polygons.append(create_rectangle(x + first_y_offset + i*repeating_y_offset, y + y_offset_rectangles, 
                                                       rectangle_height, rectangle_width, 
                                                       layer_data))
            alignment_polygons.append(create_rectangle(x - first_y_offset - i*repeating_y_offset, y + y_offset_rectangles, 
                                                       rectangle_height, rectangle_width, 
                                                       layer_data))
    
    
    
    return alignment_polygons

def create_one_a_mark(x, y,
                      thickness, length,
                      layer_data):
    
    return create_alignment_mark(x, y,
                                 thickness, length,
                                 0, 0,
                                 0, 0,
                                 0, 0, 0,
                                 False,
                                 layer_data)


def create_alignment_top_left(x, y, 
                           number_of_marks,
                           x_offset, y_offset,
                           layer_data):
    
    alignment_polygons = []
    
    thickness = 8
    length    = 200
    
    rectangle_width = 30
    rectangle_height = 15
    
    
    x_offset_rectangles = 190
    y_offset_rectangles = 190
    
    first_y_offset = 25
    repeating_y_offset = 30
    marks_y_direction = 5      

    with_rectangle_upper_row = [True, False, False, False]    
    with_rectangle_lower_row = [True, False, False, False]   
                          
    for i in range(number_of_marks):
        alignment_polygons = alignment_polygons + create_alignment_mark(x + i*x_offset, y,
                                                                        thickness, length,
                                                                        x_offset_rectangles, y_offset_rectangles,
                                                                        rectangle_width, rectangle_height,
                                                                        first_y_offset, repeating_y_offset, marks_y_direction,
                                                                        with_rectangle_upper_row[i],
                                                                        layer_data)
    for i in range(number_of_marks):
        alignment_polygons = alignment_polygons + create_alignment_mark(x + i*x_offset, y + y_offset,
                                                                        thickness, length,
                                                                        x_offset_rectangles, y_offset_rectangles,
                                                                        rectangle_width, rectangle_height,
                                                                        first_y_offset, repeating_y_offset, marks_y_direction,
                                                                        with_rectangle_lower_row[i],
                                                                        layer_data)  
        
    return alignment_polygons

def create_alignment_top_right(x, y, 
                           number_of_marks,
                           x_offset, y_offset,
                           layer_data):
    
    alignment_polygons = []
    
    thickness = 8
    length    = 200
    
    rectangle_width = 30
    rectangle_height = 15
    
    
    x_offset_rectangles = -190
    y_offset_rectangles = 190
    
    first_y_offset = 25
    repeating_y_offset = 30
    marks_y_direction = 5
    
    with_rectangle_upper_row = [True, False, False, False]    
    with_rectangle_lower_row = [True, False, False, False]   
    
    for i in range(number_of_marks):
        alignment_polygons = alignment_polygons + create_alignment_mark(x + i*x_offset, y,
                                                                        thickness, length,
                                                                        x_offset_rectangles, y_offset_rectangles,
                                                                        rectangle_width, rectangle_height,
                                                                        first_y_offset, repeating_y_offset, marks_y_direction,
                                                                        with_rectangle_upper_row[i],
                                                                        layer_data)
    for i in range(number_of_marks):
        alignment_polygons = alignment_polygons + create_alignment_mark(x + i*x_offset, y + y_offset,
                                                                        thickness, length,
                                                                        x_offset_rectangles, y_offset_rectangles,
                                                                        rectangle_width, rectangle_height,
                                                                        first_y_offset, repeating_y_offset, marks_y_direction,
                                                                        with_rectangle_lower_row[i],
                                                                        layer_data)  
        
    return alignment_polygons

def create_all_alignement_marks(frame_size_x, frame_size_y,
                                row_number,
                                x_offset, y_offset,
                                frame_margin_x, frame_margin_y,
                                layer_data):
    
    all_alignment_marks = []
    
    alignment_mark_x = -frame_size_x/2 + frame_margin_x
    alignment_mark_y = frame_size_y/2 - frame_margin_y
    
    alignment_mark = create_alignment_top_left(alignment_mark_x, alignment_mark_y, 
                                           row_number,
                                           x_offset, -y_offset,
                                           layer_data)
    
    all_alignment_marks = all_alignment_marks + alignment_mark
    
    alignment_mark_bottom_right = create_alignment_top_left(alignment_mark_x, alignment_mark_y, 
                                                            row_number,
                                                            x_offset, -y_offset,
                                                            layer_data)
    for i in alignment_mark_bottom_right:
        all_alignment_marks.append(i.rotate(np.pi))
        
        
        
    alignment_mark_x = frame_size_x/2 - frame_margin_x
    alignment_mark_y = frame_size_y/2 - frame_margin_y
    
    alignment_mark = create_alignment_top_right(alignment_mark_x, alignment_mark_y, 
                                                row_number,
                                                -x_offset, -y_offset,
                                                layer_data)
    
    all_alignment_marks = all_alignment_marks + alignment_mark
    
    alignment_mark_bottom_left = create_alignment_top_right(alignment_mark_x, alignment_mark_y, 
                                                            row_number,
                                                            -x_offset, -y_offset,
                                                            layer_data)
    for i in alignment_mark_bottom_left:
        all_alignment_marks.append(i.rotate(np.pi))
        

    
    
    return all_alignment_marks
    
    
def create_orientation_arrow(x, y,
                             arrow_head, arrow_base,
                             layer_data):
    
    
    return gdstk.Polygon([(x - arrow_head/2, y),
                          (x - arrow_head, y),
                          (x,                y + arrow_head),
                          (x + arrow_head,   y),
                          (x + arrow_head/2, y),
                          (x + arrow_head/2, y - arrow_base),
                          (x - arrow_head/2, y - arrow_base)],
                           layer=layer_data['layer'],
                           datatype=layer_data['datatype'])

def create_TLM_p_circles(x, y, layer_data, circle_tolerance):
    TLM_circle_layers = []
    
    TLM_circles_x_size = 1100
    TLM_circles_y_size = 200
    TLM_circles = create_rectangle(x, y, TLM_circles_x_size, TLM_circles_y_size, layer_data['p_ring'])
    
    x_offset = -400
    middle_circle_x = x + x_offset
    x_offset = np.array([0, 200, 200, 200, 200])
    
    
    inner_annulus = 50
    outer_annulus = np.array([75, 70, 65, 60, 55])

    
    for i, x_offset in enumerate(x_offset):
        middle_circle_x = middle_circle_x + x_offset
    
        middle_annulus = create_annulus(middle_circle_x, y, 
                                        inner_annulus, outer_annulus[i], 
                                        layer_data['p_ring'], circle_tolerance)
        
        TLM_circles = gdstk.boolean(TLM_circles, middle_annulus, 'not', 
                                    layer=layer_data['p_ring']['layer'],
                                    datatype=layer_data['p_ring']['datatype'])
    
    TLM_circle_layers = TLM_circle_layers + TLM_circles
    
    
    cover_margin_x = 10
    cover_margin_y = 10
    
    cover_size_x = TLM_circles_x_size + cover_margin_x
    cover_size_y = TLM_circles_y_size + cover_margin_y
    mesa_cover = create_rectangle(x, y, cover_size_x, cover_size_y, layer_data['mesa'])
    TLM_circle_layers.append(mesa_cover)
    
    open_etch = create_rectangle(x, y, cover_size_x, cover_size_y, layer_data['open_contacts'])
    TLM_circle_layers.append(open_etch)
    
    
    contact_margin = 10
    TLM_contact_x_size = TLM_circles_x_size - contact_margin
    TLM_contact_y_size = TLM_circles_y_size - contact_margin
    
    TLM_contact = create_rectangle(x, y, TLM_contact_x_size, TLM_contact_y_size, layer_data['contact_pads'])
    
    contact_annulus_margin = 5
    contact_inner_annulus = inner_annulus - contact_annulus_margin
    contact_outer_annulus = outer_annulus + contact_annulus_margin
    
    ## NEED TO RESET VARIABLE THIS IS STUPID
    x_offset = -400
    middle_circle_x = x + x_offset
    x_offset = np.array([0, 200, 200, 200, 200])
    
    for i, x_offset in enumerate(x_offset):
        middle_circle_x = middle_circle_x + x_offset
    
        middle_annulus = create_annulus(middle_circle_x, y, 
                                        contact_inner_annulus, contact_outer_annulus[i], 
                                        layer_data['contact_pads'], circle_tolerance)
        
        TLM_contact = gdstk.boolean(TLM_contact, middle_annulus, 'not', 
                                    layer=layer_data['contact_pads']['layer'],
                                    datatype=layer_data['contact_pads']['datatype'])
    
    
    TLM_circle_layers = TLM_circle_layers + TLM_contact
    
    return TLM_circle_layers

def create_TLM_n_circles(x, y, layer_data, circle_tolerance):
    TLM_circle_layers = []
    
    TLM_circles_x_size = 1100
    TLM_circles_y_size = 200
    TLM_circles = create_rectangle(x, y, TLM_circles_x_size, TLM_circles_y_size, layer_data['n_ring'])
    
    x_offset = -400
    middle_circle_x = x + x_offset
    x_offset = np.array([0, 200, 200, 200, 200])
    
    
    inner_annulus = 50
    outer_annulus = np.array([75, 70, 65, 60, 55])

    
    for i, x_offset in enumerate(x_offset):
        middle_circle_x = middle_circle_x + x_offset
    
        middle_annulus = create_annulus(middle_circle_x, y, inner_annulus, outer_annulus[i], layer_data['n_ring'], circle_tolerance)
        
        TLM_circles = gdstk.boolean(TLM_circles, middle_annulus, 'not', 
                                    layer=layer_data['n_ring']['layer'],
                                    datatype=layer_data['n_ring']['datatype'])
    
    TLM_circle_layers = TLM_circle_layers + TLM_circles
    
    
    cover_margin_x = 10
    cover_margin_y = 10
    
    cover_size_x = TLM_circles_x_size + cover_margin_x
    cover_size_y = TLM_circles_y_size + cover_margin_y
    mesa_cover = create_rectangle(x, y, cover_size_x, cover_size_y, layer_data['open_contacts'])
    
    TLM_circle_layers.append(mesa_cover)
    
    contact_margin = 10
    TLM_contact_x_size = TLM_circles_x_size - contact_margin
    TLM_contact_y_size = TLM_circles_y_size - contact_margin
    
    TLM_contact = create_rectangle(x, y, TLM_contact_x_size, TLM_contact_y_size, layer_data['contact_pads'])
    
    contact_annulus_margin = 5
    contact_inner_annulus = inner_annulus - contact_annulus_margin
    contact_outer_annulus = outer_annulus + contact_annulus_margin
    
    ## NEED TO RESET VARIABLE THIS IS STUPID
    x_offset = -400
    middle_circle_x = x + x_offset
    x_offset = np.array([0, 200, 200, 200, 200])
    
    for i, x_offset in enumerate(x_offset):
        middle_circle_x = middle_circle_x + x_offset
    
        middle_annulus = create_annulus(middle_circle_x, y, 
                                        contact_inner_annulus, contact_outer_annulus[i], 
                                        layer_data['contact_pads'], circle_tolerance)
        
        TLM_contact = gdstk.boolean(TLM_contact, middle_annulus, 'not', 
                                    layer=layer_data['contact_pads']['layer'],
                                    datatype=layer_data['contact_pads']['datatype'])
    
    
    TLM_circle_layers = TLM_circle_layers + TLM_contact
    
    return TLM_circle_layers

def TLM_p_pads(x, y, layer_data):
    TLM_pads = []
    
    pad_width = 80
    pad_height = 100
    
    x_first_offset  = -75
    x_second_offset = -160
    x_third_offset  = -245
    x_fourth_offset = -335
    x_fifth_offset  = -430
    
    x_positions = [x,
                   x + x_first_offset,
                   x + x_second_offset,
                   x + x_third_offset,
                   x + x_fourth_offset,
                   x + x_fifth_offset]
    
    for x_pads in x_positions:
    
        TLM_pads.append(create_rectangle(x_pads, y, pad_width, pad_height, layer_data['p_ring']))
        
    
    cover_margin_x = 10
    cover_margin_y = 10
    
    cover_size_x = -x_fifth_offset + pad_width + cover_margin_x
    cover_size_y = pad_height + cover_margin_y
    mesa_cover = create_rectangle(x + x_fifth_offset/2, y, cover_size_x, cover_size_y, layer_data['mesa'])
    
    TLM_pads.append(mesa_cover)
    
    open_etch = create_rectangle(x + x_fifth_offset/2, y, cover_size_x, cover_size_y, layer_data['open_contacts'])
    
    TLM_pads.append(open_etch)
    
    
    contact_margin = 10
    contact_width = pad_width - contact_margin
    contact_height = pad_height - contact_margin
    for x_pads in x_positions:
    
        TLM_pads.append(create_rectangle(x_pads, y, contact_width, contact_height, layer_data['contact_pads']))
    
    
    return TLM_pads

def TLM_n_pads(x, y, layer_data):
    TLM_pads = []
    
    pad_width = 80
    pad_height = 100
    
    x_first_offset  = -75
    x_second_offset = -160
    x_third_offset  = -245
    x_fourth_offset = -335
    x_fifth_offset  = -430
    
    x_positions = [x,
                   x + x_first_offset,
                   x + x_second_offset,
                   x + x_third_offset,
                   x + x_fourth_offset,
                   x + x_fifth_offset]
    
    for x_pads in x_positions:
    
        TLM_pads.append(create_rectangle(x_pads, y, pad_width, pad_height, layer_data['n_ring']))
        
    
    cover_margin_x = 10
    cover_margin_y = 10
    
    cover_size_x = -x_fifth_offset + pad_width + cover_margin_x
    cover_size_y = pad_height + cover_margin_y
    mesa_cover = create_rectangle(x + x_fifth_offset/2, y, cover_size_x, cover_size_y, layer_data['open_contacts'])
    
    TLM_pads.append(mesa_cover)
    
    contact_margin = 10
    contact_width = pad_width - contact_margin
    contact_height = pad_height - contact_margin
    for x_pads in x_positions:
    
        TLM_pads.append(create_rectangle(x_pads, y, contact_width, contact_height, layer_data['contact_pads']))
    
    
    return TLM_pads


def create_upper_a_mark_cover(x, y,
                     frame_size_x, frame_size_y,
                     a_mark_x_offset, a_mark_y_offset,
                     frame_margin_default,
                     frame_margin_x, frame_margin_y,
                     layer_data):

    x_margin_offset = frame_margin_default - frame_margin_x
    y_margin_offset = frame_margin_default - frame_margin_y
    
    cover_upper_marks = gdstk.Polygon([(-frame_size_x/2,  frame_size_y/2),
                                       (frame_size_x/2,   frame_size_y/2),
                                       (frame_size_x/2,   frame_size_y/2 - 2*a_mark_y_offset + y_margin_offset),
                                       (-frame_size_x/2,  frame_size_y/2 - 2*a_mark_y_offset + y_margin_offset),
                                       (-frame_size_x/2,  frame_size_y/2 - a_mark_y_offset + y_margin_offset)],
                                       layer=layer_data['layer'],
                                       datatype=layer_data['datatype'])
    
    return cover_upper_marks

def cover_upper_mesa(x, y,
                     frame_size_x, frame_size_y,
                     a_mark_x_offset, a_mark_y_offset,
                     frame_margin_default,
                     frame_margin_x, frame_margin_y,
                     layer_data):
    
    cover_upper_marks =  create_upper_a_mark_cover(x, y,
                                                   frame_size_x, frame_size_y,
                                                   a_mark_x_offset, a_mark_y_offset,
                                                   frame_margin_default,
                                                   frame_margin_x, frame_margin_y,
                                                   layer_data)
    
    remove_left_a_mark = create_rectangle(-frame_size_x/2 + a_mark_x_offset/2, frame_size_y/2 - a_mark_x_offset/2 - a_mark_x_offset, 
                                          a_mark_x_offset, a_mark_y_offset, layer_data)
    
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, remove_left_a_mark, 'not',
                                      layer=layer_data['layer'],
                                      datatype=layer_data['datatype'])
    
    cover_upper_marks = cover_upper_marks[0]
    
    
    remove_right_a_mark = create_rectangle(frame_size_x/2 - a_mark_x_offset/2, frame_size_y/2 - a_mark_x_offset/2 - a_mark_x_offset, 
                                          a_mark_x_offset, a_mark_y_offset, layer_data)
    
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, remove_right_a_mark, 'not',
                                      layer=layer_data['layer'],
                                      datatype=layer_data['datatype'])
    
    cover_upper_marks = cover_upper_marks[0]
    return cover_upper_marks

def cover_upper_MS_alignment(x, y,
                            frame_size_x, frame_size_y,
                            a_mark_x_offset, a_mark_y_offset,
                            frame_margin_default,
                            frame_margin_x, frame_margin_y,
                            layer_data):
    
    cover_upper_marks = []
    
    cover_upper_marks =  create_upper_a_mark_cover(x, y,
                                                   frame_size_x, frame_size_y,
                                                   a_mark_x_offset, a_mark_y_offset,
                                                   frame_margin_default,
                                                   frame_margin_x, frame_margin_y,
                                                   layer_data)
    
    remove_left_a_mark = create_rectangle(-frame_size_x/2 + a_mark_x_offset/2, frame_size_y/2 - a_mark_x_offset/2, 
                                          a_mark_x_offset, a_mark_y_offset, layer_data)
    
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, remove_left_a_mark, 'not',
                                      layer=layer_data['layer'],
                                      datatype=layer_data['datatype'])
    
    cover_upper_marks = cover_upper_marks + cover_upper_marks
    
    
    remove_right_a_mark = create_rectangle(frame_size_x/2 - a_mark_x_offset/2, frame_size_y/2, 
                                          a_mark_x_offset, 2*a_mark_y_offset, layer_data)
    
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, remove_right_a_mark, 'not',
                                      layer=layer_data['layer'],
                                      datatype=layer_data['datatype'])
    
    return cover_upper_marks

def cover_upper_open_contacts(x, y,
                              frame_size_x, frame_size_y,
                              a_mark_x_offset, a_mark_y_offset,
                              frame_margin_default,
                              frame_margin_x, frame_margin_y,
                              layer_data):
    
    upper_marks = []
    
    cover_upper_marks =  create_upper_a_mark_cover(x, y,
                                               frame_size_x, frame_size_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               frame_margin_default,
                                               frame_margin_x, frame_margin_y,
                                               layer_data)
    
    left_a_mark_x = -frame_size_x/2 + a_mark_x_offset/2 + 2*a_mark_x_offset
    left_a_mark_y = frame_size_y/2 - a_mark_x_offset/2 - a_mark_y_offset
    
    
    remove_left_a_mark = create_rectangle(left_a_mark_x, left_a_mark_y, 
                                          a_mark_x_offset, a_mark_y_offset, layer_data)
    
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, remove_left_a_mark, 'not',
                                      layer=layer_data['layer'],
                                      datatype=layer_data['datatype'])
    
    cover_upper_marks = cover_upper_marks[0]
    
    right_a_mark_x = frame_size_x/2 - a_mark_x_offset/2 - 2*a_mark_x_offset
    right_a_mark_y = frame_size_y/2 - a_mark_x_offset/2 - a_mark_y_offset
    
    
    remove_right_a_mark = create_rectangle(right_a_mark_x, right_a_mark_y, 
                                           a_mark_x_offset, a_mark_y_offset, layer_data)
    
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, remove_right_a_mark, 'not',
                                      layer=layer_data['layer'],
                                      datatype=layer_data['datatype'])
    
    upper_marks.append(cover_upper_marks[0])
    
    thickness = 24
    length    = 200 
    left_a_mark = create_one_a_mark(left_a_mark_x, left_a_mark_y, 
                                    thickness, length, 
                                    layer_data)
    
    
    thickness_remove = 12
    left_a_mark_remove = create_one_a_mark(left_a_mark_x, left_a_mark_y, 
                                           thickness_remove, length, 
                                           layer_data)
    
    left_a_mark = gdstk.boolean(left_a_mark, left_a_mark_remove, 'not',
                                layer=layer_data['layer'],
                                datatype=layer_data['datatype'])
    
    upper_marks.append(left_a_mark[0])
    
    
    right_a_mark = create_one_a_mark(right_a_mark_x, right_a_mark_y, 
                                    thickness, length, 
                                    layer_data)
    
    thickness_remove = 12
    right_a_mark_remove = create_one_a_mark(right_a_mark_x, right_a_mark_y, 
                                            thickness_remove, length, 
                                            layer_data)
    right_a_mark_remove
    right_a_mark = gdstk.boolean(right_a_mark, right_a_mark_remove, 'not',
                                layer=layer_data['layer'],
                                datatype=layer_data['datatype'])
    
    upper_marks.append(right_a_mark[0])
    
    return upper_marks



def cover_lower_mesa(x, y,
                     frame_size_x, frame_size_y,
                     row_number,
                     a_mark_x_offset, a_mark_y_offset,
                     frame_margin_default,
                     frame_margin_x, frame_margin_y,
                     layer_data):
    
    upper_mesa_cover = cover_upper_mesa(x, y,
                                        frame_size_x, frame_size_y,
                                        a_mark_x_offset, a_mark_y_offset,
                                        frame_margin_default,
                                        frame_margin_x, frame_margin_y,
                                        layer_data)
    
    upper_mesa_cover.rotate(np.pi)
    
    lower_cutout = create_rectangle(0, 0, frame_size_x - a_mark_x_offset*row_number*2, frame_size_y, layer_data)
    
    upper_mesa_cover = gdstk.boolean(upper_mesa_cover, lower_cutout, 'not',
                                                layer=layer_data['layer'], datatype=layer_data['datatype'])
    
    return upper_mesa_cover

def cover_lower_MS_alignment(x, y,
                     frame_size_x, frame_size_y,
                     row_number,
                     a_mark_x_offset, a_mark_y_offset,
                     frame_margin_default,
                     frame_margin_x, frame_margin_y,
                     layer_data):
    
    upper_mesa_cover = cover_upper_MS_alignment(x, y,
                                        frame_size_x, frame_size_y,
                                        a_mark_x_offset, a_mark_y_offset,
                                        frame_margin_default,
                                        frame_margin_x, frame_margin_y,
                                        layer_data)

    for i in upper_mesa_cover:
        i.rotate(np.pi)
    
    lower_cutout = create_rectangle(0, 0, frame_size_x - a_mark_x_offset*row_number*2, frame_size_y, layer_data)
    
    upper_mesa_cover = gdstk.boolean(upper_mesa_cover, lower_cutout, 'not',
                                                layer=layer_data['layer'], datatype=layer_data['datatype'])
    
    return upper_mesa_cover

def cover_lower_open_contacts(x, y,
                              frame_size_x, frame_size_y,
                              row_number,
                              a_mark_x_offset, a_mark_y_offset,
                              frame_margin_default,
                              frame_margin_x, frame_margin_y,
                              layer_data):
    
    upper_open_contact_marks = []
    
    upper_open_contact_cover = cover_upper_open_contacts(x, y,
                                                         frame_size_x, frame_size_y,
                                                         a_mark_x_offset, a_mark_y_offset,
                                                         frame_margin_default,
                                                         frame_margin_x, frame_margin_y,
                                                         layer_data)
    
            
    for i in upper_open_contact_cover:
        
        i.rotate(np.pi)
        
        lower_cutout = create_rectangle(0, 0, frame_size_x - a_mark_x_offset*row_number*2, frame_size_y, layer_data)
        
        upper_open_contact_cover = gdstk.boolean(i, lower_cutout, 'not',
                                                 layer=layer_data['layer'], 
                                                 datatype=layer_data['datatype'])
        
        
        upper_open_contact_marks = upper_open_contact_marks + upper_open_contact_cover
        
    
    return upper_open_contact_marks

def cover_a_mark_mesa(frame_size_x, frame_size_y,
                      x_offset, y_offset,
                      frame_margin_x, frame_margin_y,
                      a_mark_x_offset, a_mark_y_offset,
                      layer_data):
    length = 200
    thickness = 24
    
    a_mark = create_one_a_mark(-frame_size_x/2 + frame_margin_x + x_offset, frame_size_y/2 - frame_margin_y - a_mark_y_offset + y_offset,
                               thickness, length,
                               layer_data)
    
    length_cutout    = 200
    thickness_cutout = 12
    
    
    a_mark_cutout = create_one_a_mark(-frame_size_x/2 + frame_margin_x + x_offset , frame_size_y/2 - frame_margin_y - a_mark_y_offset + y_offset,
                               thickness_cutout, length_cutout,
                               layer_data)
    
    a_mark = gdstk.boolean(a_mark, a_mark_cutout, 'not',
                           layer=layer_data['layer'], datatype=layer_data['datatype'])
    
    return a_mark

def cover_a_mark_MS_align(frame_size_x, frame_size_y,
                      x_offset, y_offset,
                      frame_margin_x, frame_margin_y,
                      a_mark_x_offset, a_mark_y_offset,
                      layer_data):
    length = 200
    thickness = 24
    
    a_mark = create_one_a_mark(-frame_size_x/2 + frame_margin_x + x_offset, frame_size_y/2 - frame_margin_y + y_offset,
                               thickness, length,
                               layer_data)
    
    length_cutout    = 200
    thickness_cutout = 12
    
    
    a_mark_cutout = create_one_a_mark(-frame_size_x/2 + frame_margin_x + x_offset , frame_size_y/2 - frame_margin_y + y_offset,
                               thickness_cutout, length_cutout,
                               layer_data)
    
    a_mark = gdstk.boolean(a_mark, a_mark_cutout, 'not',
                           layer=layer_data['layer'], datatype=layer_data['datatype'])
    
    return a_mark

def create_rectangles_a_mark_mesa(frame_size_x, frame_size_y,
                                  frame_margin_x, frame_margin_y,
                                  a_mark_x_offset, a_mark_y_offset,
                                  rectangles_to_the_left,
                                  layer_data):
    all_rectangles = []
    
    rectangle_width = 30
    rectangle_height = 15
    
    if rectangles_to_the_left:
        x_offset_rectangles = -175
    else:
        x_offset_rectangles = 175
        
    y_offset_rectangles = 175
    
    first_y_offset = 25
    extra_y_offset = np.array([0.5, 1, 1.5, 2, 2.5])
    repeating_y_offset = 30
    marks_y_direction = 5
    
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x + x_offset_rectangles, frame_size_y/2 - frame_margin_y - a_mark_y_offset - first_y_offset - i*repeating_y_offset - extra_y_offset[i],
                                       rectangle_width, rectangle_height, layer_data['mesa'])
        all_rectangles.append(a_rectangle)
        
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x + x_offset_rectangles, frame_size_y/2 - frame_margin_y - a_mark_y_offset + first_y_offset + i*repeating_y_offset + extra_y_offset[i],
                                       rectangle_width, rectangle_height, layer_data['mesa'])
        all_rectangles.append(a_rectangle)
        
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x + first_y_offset + i*repeating_y_offset + extra_y_offset[i], frame_size_y/2 - frame_margin_y - a_mark_y_offset + y_offset_rectangles,
                                       rectangle_height, rectangle_width, layer_data['mesa'])
        all_rectangles.append(a_rectangle)
        
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x - first_y_offset - i*repeating_y_offset - extra_y_offset[i], frame_size_y/2 - frame_margin_y - a_mark_y_offset + y_offset_rectangles,
                                       rectangle_height, rectangle_width, layer_data['mesa'])
        all_rectangles.append(a_rectangle)
        
    return all_rectangles

def create_rectangles_a_mark_MS_align(frame_size_x, frame_size_y,
                                      frame_margin_x, frame_margin_y,
                                      a_mark_x_offset, a_mark_y_offset,
                                      rectangles_to_the_left,
                                      layer_data):
    all_rectangles = []
    
    rectangle_width = 30
    rectangle_height = 15
    
    if rectangles_to_the_left:
        x_offset_rectangles = -175
    else:
        x_offset_rectangles = 175
        
    y_offset_rectangles = 175
    
    first_y_offset = 25
    extra_y_offset = np.array([0.5, 1, 1.5, 2, 2.5])
    repeating_y_offset = 30
    marks_y_direction = 5

    
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x + x_offset_rectangles, frame_size_y/2 - frame_margin_y - first_y_offset - i*repeating_y_offset - extra_y_offset[i],
                                       rectangle_width, rectangle_height, layer_data['MS_align'])
        all_rectangles.append(a_rectangle)
        
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x + x_offset_rectangles, frame_size_y/2 - frame_margin_y + first_y_offset + i*repeating_y_offset + extra_y_offset[i],
                                       rectangle_width, rectangle_height, layer_data['MS_align'])
        all_rectangles.append(a_rectangle)
        
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x + first_y_offset + i*repeating_y_offset + extra_y_offset[i], frame_size_y/2 - frame_margin_y + y_offset_rectangles,
                                       rectangle_height, rectangle_width, layer_data['MS_align'])
        all_rectangles.append(a_rectangle)
        
    for i in range(marks_y_direction):
        a_rectangle = create_rectangle(-frame_size_x/2 + frame_margin_x - first_y_offset - i*repeating_y_offset - extra_y_offset[i], frame_size_y/2 - frame_margin_y + y_offset_rectangles,
                                       rectangle_height, rectangle_width, layer_data['MS_align'])
        all_rectangles.append(a_rectangle)
        
    return all_rectangles
    
def create_all_a_mark_mesa(frame_size_x, frame_size_y,
                                frame_margin_x, frame_margin_y,
                                a_mark_x_offset, a_mark_y_offset,
                                layer_data):
        
    all_a_marks = []

    a_mark = cover_a_mark_mesa(frame_size_x, frame_size_y,
                               0, 0,
                               frame_margin_x, frame_margin_y,
                               a_mark_x_offset, a_mark_y_offset,
                               layer_data['mesa'])
    
    all_a_marks.append(*a_mark)

    a_mark = cover_a_mark_mesa(frame_size_x, frame_size_y,
                           0, 0,
                           frame_margin_x, frame_margin_y,
                           a_mark_x_offset, a_mark_y_offset,
                           layer_data['mesa'])

    a_mark = a_mark[0].rotate(np.pi)
    all_a_marks.append(a_mark)


    a_mark = cover_a_mark_mesa(frame_size_x, frame_size_y,
                               frame_size_x, 0,
                               -frame_margin_x, frame_margin_y,
                               a_mark_x_offset, a_mark_y_offset,
                               layer_data['mesa'])
    
    all_a_marks.append(*a_mark)
   
    a_mark = cover_a_mark_mesa(frame_size_x, frame_size_y,
                               frame_size_x, 0,
                               -frame_margin_x, frame_margin_y,
                               a_mark_x_offset, a_mark_y_offset,
                               layer_data['mesa'])

    a_mark = a_mark[0].rotate(np.pi)
    all_a_marks.append(a_mark)
    
    small_x_offset = 120
    small_y_offset = 120
    
    small_a_mark_thickness = 8
    small_a_mark_length    = 100
    a_mark_cutout = create_one_a_mark(-frame_size_x/2 + frame_margin_x + small_x_offset, frame_size_y/2 - frame_margin_y - a_mark_y_offset - small_y_offset,
                       small_a_mark_thickness, small_a_mark_length,
                       layer_data['mesa'])
    
    all_a_marks.append(a_mark_cutout[0])
    
    a_mark_cutout = create_one_a_mark(-frame_size_x/2 + frame_margin_x + small_x_offset, frame_size_y/2 - frame_margin_y - a_mark_y_offset - small_y_offset,
                       small_a_mark_thickness, small_a_mark_length,
                       layer_data['mesa'])
    
    a_mark_cutout = a_mark_cutout[0].rotate(np.pi)
    all_a_marks.append(a_mark_cutout)
    
    a_mark_cutout = create_one_a_mark(frame_size_x/2 - frame_margin_x - small_x_offset, frame_size_y/2 - frame_margin_y - a_mark_y_offset - small_y_offset,
                       small_a_mark_thickness, small_a_mark_length,
                       layer_data['mesa'])
    
    all_a_marks.append(a_mark_cutout[0])
    
    a_mark_cutout = create_one_a_mark(frame_size_x/2 - frame_margin_x - small_x_offset, frame_size_y/2 - frame_margin_y - a_mark_y_offset - small_y_offset,
                       small_a_mark_thickness, small_a_mark_length,
                       layer_data['mesa'])
    
    a_mark_cutout = a_mark_cutout[0].rotate(np.pi)
    all_a_marks.append(a_mark_cutout)
    

        
    rectangles_to_the_left = True
    rectangles = create_rectangles_a_mark_mesa(frame_size_x, frame_size_y,
                                               frame_margin_x, frame_margin_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               rectangles_to_the_left,
                                               layer_data)
        
    all_a_marks = all_a_marks + rectangles
    
    rectangles = create_rectangles_a_mark_mesa(frame_size_x, frame_size_y,
                                               frame_margin_x, frame_margin_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               rectangles_to_the_left,
                                               layer_data)
    
    for i in rectangles:
        all_a_marks.append(i.rotate(np.pi))
    
    
    
    rectangles_to_the_left = False
    rectangles = create_rectangles_a_mark_mesa(-frame_size_x, frame_size_y,
                                                -frame_margin_x, frame_margin_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                rectangles_to_the_left,
                                                layer_data)
    all_a_marks = all_a_marks + rectangles
    
    rectangles = create_rectangles_a_mark_mesa(-frame_size_x, frame_size_y,
                                               -frame_margin_x, frame_margin_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               rectangles_to_the_left,
                                               layer_data)
    
    for i in rectangles:
        all_a_marks.append(i.rotate(np.pi))
    
    return all_a_marks

def create_all_a_mark_MS_align(frame_size_x, frame_size_y,
                                frame_margin_x, frame_margin_y,
                                a_mark_x_offset, a_mark_y_offset,
                                layer_data):
        
    all_a_marks = []

    a_mark = cover_a_mark_MS_align(frame_size_x, frame_size_y,
                                   0, 0,
                                   frame_margin_x, frame_margin_y,
                                   a_mark_x_offset, a_mark_y_offset,
                                   layer_data['MS_align'])
    
    all_a_marks.append(*a_mark)

    a_mark = cover_a_mark_MS_align(frame_size_x, frame_size_y,
                                   0, 0,
                                   frame_margin_x, frame_margin_y,
                                   a_mark_x_offset, a_mark_y_offset,
                                   layer_data['MS_align'])

    a_mark = a_mark[0].rotate(np.pi)
    all_a_marks.append(a_mark)


    a_mark = cover_a_mark_MS_align(frame_size_x, frame_size_y,
                                   frame_size_x, 0,
                                   -frame_margin_x, frame_margin_y,
                                   -a_mark_x_offset, a_mark_y_offset,
                                   layer_data['MS_align'])
    
    all_a_marks.append(*a_mark)
   
    a_mark = cover_a_mark_MS_align(frame_size_x, frame_size_y,
                                   frame_size_x, 0,
                                   -frame_margin_x, frame_margin_y,
                                   -a_mark_x_offset, a_mark_y_offset,
                                   layer_data['MS_align'])

    a_mark = a_mark[0].rotate(np.pi)
    all_a_marks.append(a_mark)
    
    small_x_offset = 120
    small_y_offset = 120
    
    small_a_mark_thickness = 8
    small_a_mark_length    = 100
    a_mark_cutout = create_one_a_mark(-frame_size_x/2 + frame_margin_x + small_x_offset, frame_size_y/2 - frame_margin_y - small_y_offset,
                                      small_a_mark_thickness, small_a_mark_length,
                                      layer_data['MS_align'])
    
    all_a_marks.append(a_mark_cutout[0])
    
    a_mark_cutout = create_one_a_mark(-frame_size_x/2 + frame_margin_x + small_x_offset, frame_size_y/2 - frame_margin_y - small_y_offset,
                                      small_a_mark_thickness, small_a_mark_length,
                                      layer_data['MS_align'])
    
    a_mark_cutout = a_mark_cutout[0].rotate(np.pi)
    all_a_marks.append(a_mark_cutout)
    
    a_mark_cutout = create_one_a_mark(frame_size_x/2 - frame_margin_x - small_x_offset, frame_size_y/2 - frame_margin_y - small_y_offset,
                                      small_a_mark_thickness, small_a_mark_length,
                                      layer_data['MS_align'])
    
    all_a_marks.append(a_mark_cutout[0])
    
    a_mark_cutout = create_one_a_mark(frame_size_x/2 - frame_margin_x - small_x_offset, frame_size_y/2 - frame_margin_y - small_y_offset,
                                      small_a_mark_thickness, small_a_mark_length,
                                      layer_data['MS_align'])
    
    a_mark_cutout = a_mark_cutout[0].rotate(np.pi)
    all_a_marks.append(a_mark_cutout)
    

        
    rectangles_to_the_left = True
    rectangles = create_rectangles_a_mark_MS_align(frame_size_x, frame_size_y,
                                                   frame_margin_x, frame_margin_y,
                                                   a_mark_x_offset, a_mark_y_offset,
                                                   rectangles_to_the_left,
                                                   layer_data)
        
    all_a_marks = all_a_marks + rectangles
    
    rectangles = create_rectangles_a_mark_MS_align(frame_size_x, frame_size_y,
                                                   frame_margin_x, frame_margin_y,
                                                   a_mark_x_offset, a_mark_y_offset,
                                                   rectangles_to_the_left,
                                                   layer_data)
    
    for i in rectangles:
        all_a_marks.append(i.rotate(np.pi))
    
    
    
    rectangles_to_the_left = False
    rectangles = create_rectangles_a_mark_MS_align(-frame_size_x, frame_size_y,
                                                -frame_margin_x, frame_margin_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                rectangles_to_the_left,
                                                layer_data)
    all_a_marks = all_a_marks + rectangles
    
    rectangles = create_rectangles_a_mark_MS_align(-frame_size_x, frame_size_y,
                                               -frame_margin_x, frame_margin_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               rectangles_to_the_left,
                                               layer_data)
    
    for i in rectangles:
        all_a_marks.append(i.rotate(np.pi))
        
    
    MS_center_rect = 20
    MS_arm_offset  = 160
    
    MS_arm_width   = 170
    MS_arm_height  = 10
    
    # a_mark_cutout = create_MS_EBL_alignment_list(frame_size_x/2 - frame_margin_x - 4*a_mark_x_offset, frame_size_y/2 - frame_margin_y,
    #                                               MS_center_rect, MS_arm_offset,
    #                                               MS_arm_width, MS_arm_height,
    #                                               layer_data['MS_align'])
    
    # all_a_marks = all_a_marks + a_mark_cutout
    
    # # a_mark_cutout = create_MS_EBL_alignment_list(frame_size_x/2 - frame_margin_x - 4*a_mark_x_offset, frame_size_y/2 - frame_margin_y,
    # #                                               MS_center_rect, MS_arm_offset,
    # #                                               MS_arm_width, MS_arm_height,
    # #                                               layer_data['MS_align'])
    
    # # for i in a_mark_cutout:
    # #     i.rotate(np.pi)
        
    # # all_a_marks = all_a_marks + a_mark_cutout
    
    
    
    # a_mark_cutout = create_MS_EBL_alignment_list(-frame_size_x/2 + frame_margin_x + 4*a_mark_x_offset, frame_size_y/2 - frame_margin_y,
    #                                               MS_center_rect, MS_arm_offset,
    #                                               MS_arm_width, MS_arm_height,
    #                                               layer_data['MS_align'])
    
    # all_a_marks = all_a_marks + a_mark_cutout
    
    # a_mark_cutout = create_MS_EBL_alignment_list(-frame_size_x/2 + frame_margin_x + 4*a_mark_x_offset, frame_size_y/2 - frame_margin_y,
    #                                               MS_center_rect, MS_arm_offset,
    #                                               MS_arm_width, MS_arm_height,
    #                                               layer_data['MS_align'])
    
    # for i in a_mark_cutout:
    #     i.rotate(np.pi)
        
    # all_a_marks = all_a_marks + a_mark_cutout
    
    return all_a_marks

def create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                a_mark_x_offset, a_mark_y_offset,
                                layer_data):
    cover_a_mark = []
    cover_a_mark_open = create_rectangle(cover_a_mark_x, cover_a_mark_y, 
                                         a_mark_x_offset, a_mark_y_offset, 
                                         layer_data)
    
    thickness = 24
    length    = 200
    cross_to_remove = create_alignment_mark(cover_a_mark_x, cover_a_mark_y, 
                          thickness, length, 
                          0, 0, 
                          0, 0, 
                          0, 0, 0, False, layer_data)

    cross_to_remove = cross_to_remove[0]
    cover_a_mark_open = gdstk.boolean(cover_a_mark_open, cross_to_remove, 'not', 
                                      layer=layer_data['layer'], 
                                      datatype=layer_data['datatype'])
    
    
    cover_a_mark.append(*cover_a_mark_open)
    
    thickness = 12
    
    cross_to_add = create_alignment_mark(cover_a_mark_x, cover_a_mark_y, 
                      thickness, length, 
                      0, 0, 
                      0, 0, 
                      0, 0, 0, False, layer_data)
    
    cover_a_mark.append(*cross_to_add)
    
    return cover_a_mark
    
def create_all_a_mark_open_sidewall(frame_size_x, frame_size_y,
                                    a_mark_x_offset, a_mark_y_offset,
                                    layer_data):
    all_a_mark_cover = []
    
    cover_a_mark_x = -frame_size_x/2 + 3*a_mark_x_offset/2
    cover_a_mark_y = frame_size_y/2 - 3*a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = frame_size_x/2 - 3*a_mark_x_offset/2
    cover_a_mark_y = frame_size_y/2 - 3*a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = -frame_size_x/2 + 3*a_mark_x_offset/2
    cover_a_mark_y = -frame_size_y/2 + 3*a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = frame_size_x/2 - 3*a_mark_x_offset/2
    cover_a_mark_y = -frame_size_y/2 + 3*a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    return all_a_mark_cover

def create_all_a_mark_bottom_contact(frame_size_x, frame_size_y,
                                    a_mark_x_offset, a_mark_y_offset,
                                    layer_data):
    all_a_mark_cover = []
    
    cover_a_mark_x = -frame_size_x/2 + a_mark_x_offset/2 + a_mark_x_offset
    cover_a_mark_y = frame_size_y/2 - a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = frame_size_x/2 - a_mark_x_offset/2 - a_mark_x_offset
    cover_a_mark_y = frame_size_y/2 - a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = -frame_size_x/2 + a_mark_x_offset/2 + a_mark_x_offset
    cover_a_mark_y = -frame_size_y/2 + a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = frame_size_x/2 - a_mark_x_offset/2 - a_mark_x_offset
    cover_a_mark_y = -frame_size_y/2 + a_mark_y_offset/2
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    return all_a_mark_cover

def create_all_a_mark_witness_mesa(frame_size_x, frame_size_y,
                                    a_mark_x_offset, a_mark_y_offset,
                                    layer_data):
    all_a_mark_cover = []
    
    cover_a_mark_x = -frame_size_x/2 + a_mark_x_offset/2 + 3*a_mark_x_offset
    cover_a_mark_y = frame_size_y/2 - a_mark_y_offset/2 - a_mark_y_offset
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                               a_mark_x_offset, a_mark_y_offset,
                                               layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = frame_size_x/2 - a_mark_x_offset/2 - 3*a_mark_x_offset
    cover_a_mark_y = frame_size_y/2 - a_mark_y_offset/2 - a_mark_y_offset
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = -frame_size_x/2 + a_mark_x_offset/2 + 3*a_mark_x_offset
    cover_a_mark_y = -frame_size_y/2 + a_mark_y_offset/2 + a_mark_y_offset
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    cover_a_mark_x = frame_size_x/2 - a_mark_x_offset/2 - 3*a_mark_x_offset
    cover_a_mark_y = -frame_size_y/2 + a_mark_y_offset/2 + a_mark_y_offset
    
    cover_a_mark = create_a_mark_open_sidewall(cover_a_mark_x, cover_a_mark_y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)

    all_a_mark_cover = all_a_mark_cover + cover_a_mark
    
    return all_a_mark_cover

def create_side_cover(chip_center_x, chip_center_y,
                      chip_size_x, chip_size_y,
                      frame_size_x, frame_size_y,
                      layer_data):
    cover_sides = create_rectangle(chip_center_x, chip_center_y, 
                                   chip_size_x, chip_size_y, 
                                   layer_data)
    
    frame_to_remove = create_rectangle(chip_center_x, chip_center_y, 
                                       frame_size_x, frame_size_y, 
                                       layer_data)
    
    cover_sides = gdstk.boolean(cover_sides, frame_to_remove, 'not',
                                layer=layer_data['layer'],
                                datatype=layer_data['datatype'])
    
    return cover_sides
    
def create_cover_DF_a_mark(x, y,
                           a_mark_x_offset, a_mark_y_offset, 
                           layer_data):
    
    polygons = []
    
    left_a_mark_contact_pads = create_rectangle(x, y,
                                                a_mark_x_offset, a_mark_y_offset,
                                                layer_data)
    
    
    thickness_remove = 24
    length    = 200
    a_mark_remove = create_one_a_mark(x, y, 
                                      thickness_remove, length, 
                                      layer_data)
    
    left_a_mark_contact_pads = gdstk.boolean(left_a_mark_contact_pads, a_mark_remove, 'not',
                                             layer=layer_data['layer'],
                                             datatype=layer_data['datatype'])
    
    polygons.append(*left_a_mark_contact_pads)
    
    
    
    thickness_add = 12
    a_mark_add = create_one_a_mark(x, y, 
                                   thickness_add, length, 
                                   layer_data)

    polygons.append(*a_mark_add)
    
    return polygons

# def create_MS_EBL_alignment_list(x, y,
#                                  MS_center_rect, MS_arm_offset,
#                                  MS_arm_width, MS_arm_height,
#                                  layer_data):

#     MS_marks = []
    
#     MS_center_mark = create_rectangle(x, y,
#                                       MS_center_rect, MS_center_rect,
#                                       layer_data)
    
#     MS_marks.append(MS_center_mark)
    
    
#     MS_left_arm   = create_rectangle(x - MS_arm_offset, y,
#                                      MS_arm_width, MS_arm_height,
#                                      layer_data)
    
#     MS_marks.append(MS_left_arm)
    
    
#     MS_right_arm = create_rectangle(x + MS_arm_offset, y,
#                                     MS_arm_width, MS_arm_height,
#                                     layer_data)
    
#     MS_marks.append(MS_right_arm)
    
    
#     MS_upper_arm = create_rectangle(x, y + MS_arm_offset,
#                                     MS_arm_height, MS_arm_width,
#                                     layer_data)

#     MS_marks.append(MS_upper_arm)
    
    
#     MS_lower_arm = create_rectangle(x, y - MS_arm_offset,
#                                     MS_arm_height, MS_arm_width,
#                                     layer_data)

#     MS_marks.append(MS_lower_arm)
    
#     return MS_marks
    

def create_MS_EBL_alignment(full_mask,
                            x, y,
                            MS_center_rect, MS_arm_offset,
                            MS_arm_width, MS_arm_height,
                            polgygon_VCSEL, number,
                            layer_data):

    MS_center_mark = create_rectangle(x, y,
                                      MS_center_rect, MS_center_rect,
                                      layer_data['MS_align'])

    polgygon_VCSEL['MS_center_mark' + str(number)] = MS_center_mark
    full_mask['MS_align'].add(MS_center_mark)
    
    # MS_left_arm   = create_rectangle(x - MS_arm_offset, y,
    #                                  MS_arm_width, MS_arm_height,
    #                                  layer_data['MS_align'])
    
    # polgygon_VCSEL['MS_left_arm' + str(number)] = MS_left_arm
    # full_mask['MS_align'].add(MS_left_arm)
    
    # MS_right_arm = create_rectangle(x + MS_arm_offset, y,
    #                                 MS_arm_width, MS_arm_height,
    #                                 layer_data['MS_align'])
    
    # polgygon_VCSEL['MS_right_arm' + str(number)] = MS_right_arm
    # full_mask['MS_align'].add(MS_right_arm)
    
    # MS_upper_arm = create_rectangle(x, y + MS_arm_offset,
    #                                 MS_arm_height, MS_arm_width,
    #                                 layer_data['MS_align'])
    
    # polgygon_VCSEL['MS_upper_arm' + str(number)] = MS_upper_arm
    # full_mask['MS_align'].add(MS_upper_arm)
    
    # MS_lower_arm = create_rectangle(x, y - MS_arm_offset,
    #                                 MS_arm_height, MS_arm_width,
    #                                 layer_data['MS_align'])
    
    # polgygon_VCSEL['MS_lower_arm' + str(number)] = MS_lower_arm
    # full_mask['MS_align'].add(MS_lower_arm)
    
def create_combo_mark(full_mask,
                      x, y,
                      MS_center_rect, MS_arm_offset,
                      MS_arm_width, MS_arm_height,
                      number,
                      layer_data):

    MS_center_mark = create_rectangle(x, y,
                                      MS_center_rect, MS_center_rect,
                                      layer_data['MS_align'])

    full_mask['MS_align'].add(MS_center_mark)
    
    MS_left_arm   = create_rectangle(x - MS_arm_offset, y,
                                     MS_arm_width, MS_arm_height,
                                     layer_data['MS_align'])
    
    full_mask['MS_align'].add(MS_left_arm)
    
    MS_right_arm = create_rectangle(x + MS_arm_offset, y,
                                    MS_arm_width, MS_arm_height,
                                    layer_data['MS_align'])
    
    full_mask['MS_align'].add(MS_right_arm)
    
    MS_upper_arm = create_rectangle(x, y + MS_arm_offset,
                                    MS_arm_height, MS_arm_width,
                                    layer_data['MS_align'])
    
    full_mask['MS_align'].add(MS_upper_arm)
    
    MS_lower_arm = create_rectangle(x, y - MS_arm_offset,
                                    MS_arm_height, MS_arm_width,
                                    layer_data['MS_align'])
    
    full_mask['MS_align'].add(MS_lower_arm)
    
def add_list_to_layer(list_polygon, full_mask, layer_data_reversed):
    for polygon in list_polygon:
        layer_current_polygon = layer_data_reversed[polygon.layer]
        full_mask[layer_current_polygon].add(polygon)
    
def create_one_VCSEL(full_mask, layer_data,
                     x_offset, y_offset, 
                     p_ring_inner, p_ring_outer,
                     row, column, reverse_row,
                     n_contact_outer,
                     circle_tolerance):
    
    polgygon_VCSEL = {}
    parameters_VCSEL = {}
     
    ## GEOMETRY OF DIFFERENT OBJECTS
    
    
    ## FIRST LAYER: P RING
    p_ring_x = x_offset
    p_ring_y = y_offset
    
    # Create the geometry (a single rectangle) and add it to the cell.
    p_ring = create_annulus(p_ring_x, p_ring_y,
                            p_ring_inner, p_ring_outer,
                            layer_data['p_ring'], circle_tolerance)
    
    # polgygon_VCSEL.append(p_ring)
    polgygon_VCSEL['p_ring'] = p_ring
    full_mask['p_ring'].add(p_ring)
    
    
    ## SECONDS LAYER: MESA PROTECTION
    mesa_radius = p_ring_outer + 2.0
    
    meas_x      = x_offset
    meas_y      = y_offset
    
    mesa = create_circle(meas_x, meas_y, mesa_radius, layer_data['mesa'], circle_tolerance)
    
    polgygon_VCSEL['mesa'] = mesa
    full_mask['mesa'].add(mesa)
    parameters_VCSEL['mesa_diameter'] = 2*mesa_radius
    
    
    ## THRID LAYER: OPEN SIDEWALLS FOR OXIDATION
    sidewall_inner  = mesa_radius - 4
    sidewall_outer  = mesa_radius + 5.5
    
    sidewall_x = x_offset
    sidewall_y = y_offset
    
    sidewall = create_annulus(sidewall_x, sidewall_y,
                            sidewall_inner, sidewall_outer,
                            layer_data['open_sidewalls'], circle_tolerance)
    
    # polgygon_VCSEL.append(sidewall)
    polgygon_VCSEL['sidewall'] = sidewall
    full_mask['open_sidewalls'].add(sidewall)
    
    
    
    ## FOURTH LAYER: N CONTACTS
    # n_contact_thickness = 55
    distance_from_side_opening = 5
    
    n_contact_inner  = sidewall_outer + distance_from_side_opening
    n_contact_outer  = n_contact_outer #n_contact_inner + n_contact_thickness
    
    n_contact_x      = x_offset
    n_contact_y      = y_offset
    
    # CREATE ARCH
    n_contact = create_annulus(n_contact_x, n_contact_y,
                               n_contact_inner, n_contact_outer,
                               layer_data['n_ring'], circle_tolerance)
    
    
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
                            layer=layer_data['n_ring']['layer'],
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
                           layer=layer_data['n_ring']['layer'],
                           datatype=layer_data['n_ring']['datatype'])
    n_contact = n_contact[0]
    
    # polgygon_VCSEL.append(n_contact)  
    polgygon_VCSEL['n_contact'] = n_contact
    full_mask['n_ring'].add(n_contact)
    
    
    
    ## SIXTH LAYER: OPEN CONTACTS
    ## CREATE ARCH FOR N CONTACTS
    ## THE SAME SETUP AS THE CONTACTS
    ## CREATE ANNULUS, REMOVE TRIANGLE AND SQUARE
    open_contact_margin = 2
        
    open_contacts_x = x_offset
    open_contacts_y = y_offset
    
    open_contacts_inner = n_contact_inner + open_contact_margin
    open_contacts_outer = n_contact_outer - open_contact_margin
    
    open_contact_arch = create_annulus(open_contacts_x, open_contacts_y,
                        open_contacts_inner, open_contacts_outer,
                        layer_data['n_ring'], circle_tolerance)

    
    # REMOVE TRIANGLE PART: BOOLEAN 'NOT'
    triangle_x_offset = 2 
    triangle_y_offset = open_contact_margin
    
    triangle = gdstk.Polygon([(n_contact_x - triangle_x_offset, n_contact_y + triangle_y_offset),
                              (triangle_end_x - triangle_x_offset + x_offset, -triangle_initial_end_y + triangle_y_offset + y_offset),
                              (-triangle_end_x - triangle_x_offset + x_offset, -triangle_final_end_y + triangle_y_offset + y_offset)])
    
    open_n_arch = gdstk.boolean(open_contact_arch, triangle, 'not', 
                            layer=layer_data['open_contacts']['layer'], 
                            datatype=layer_data['open_contacts']['datatype'])
    
    
    ## REMOVE SQUARE: BOOLEAN 'NOT'
    square_x_offset = square_x_offset
    square_y_offset = square_y_offset + open_contact_margin
    
    
    square = gdstk.Polygon([(-square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset,  square_side + square_y_offset),
                            (-square_side + square_x_offset,  square_side + square_y_offset)])
    
    open_n_arch = gdstk.boolean(open_n_arch, square, 'not',
                           layer=layer_data['open_contacts']['layer'],
                           datatype=layer_data['open_contacts']['datatype'])
    
    open_n_arch = open_n_arch[0]
    # polgygon_VCSEL.append(open_n_arch)    
    polgygon_VCSEL['open_n_arch'] = open_n_arch
    full_mask['open_contacts'].add(open_n_arch)
    
    
    ## CREATE CIRCLE FOR P CONTACT
    open_p_ring_margin   = 1.5
    open_p_contat_radius = p_ring_outer - open_p_ring_margin
    
    open_p_contact = create_circle(open_contacts_x, open_contacts_y,
                        open_p_contat_radius, 
                        layer_data['open_contacts'], circle_tolerance)
    
    polgygon_VCSEL['open_p_contact'] = open_p_contact
    full_mask['open_contacts'].add(open_p_contact)
    
    
    ## SEVENTH LAYER: CONTACT PADS
    contact_pad_side = 70
    contact_pad_x_offset = -50 + x_offset
    contact_pad_y_offset = -100 + y_offset
    
    probe_length = 100
    
    contact_pad_left = gdstk.Polygon([(-contact_pad_side/2 + contact_pad_x_offset, -contact_pad_side/2 + contact_pad_y_offset),
                                      ( contact_pad_side/2 + contact_pad_x_offset, -contact_pad_side/2 + contact_pad_y_offset),
                                      ( contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset),
                                      (-contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset)],
                                        layer=layer_data['contact_pads']['layer'], datatype=layer_data['contact_pads']['datatype'])
      
    polgygon_VCSEL['contact_pad_left'] = contact_pad_left
    full_mask['contact_pads'].add(contact_pad_left)
    
    
    contact_pad_right = gdstk.Polygon([(-contact_pad_side/2 + contact_pad_x_offset + probe_length, -contact_pad_side/2 + contact_pad_y_offset),
                                       ( contact_pad_side/2 + contact_pad_x_offset + probe_length, -contact_pad_side/2 + contact_pad_y_offset),
                                       ( contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset),
                                       (-contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset)],
                                        layer=layer_data['contact_pads']['layer'], datatype=layer_data['contact_pads']['datatype'])
 
    polgygon_VCSEL['contact_pad_right'] = contact_pad_right
    full_mask['contact_pads'].add(contact_pad_right)
    
    contact_pad_arch_inner  = n_contact_inner
    contact_pad_arch_outer  = n_contact_outer + 5
    
    contact_pad_x      = x_offset
    contact_pad_y      = y_offset
    
    contact_pad_arch = create_annulus(contact_pad_x, contact_pad_y,
                               contact_pad_arch_inner, contact_pad_arch_outer,
                               layer_data['contact_pads'], circle_tolerance)
    
    remove_arch_radius = contact_pad_arch_outer - 40
    
    remove_arch = create_circle(contact_pad_x, contact_pad_y,
                                remove_arch_radius, 
                                layer_data['contact_pads'], circle_tolerance)
    
    
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, remove_arch, 'not',
                                     layer=layer_data['contact_pads']['layer'],
                                     datatype=layer_data['contact_pads']['datatype'])
    
    remove_right_margin = gdstk.Polygon([(x_offset, 2*open_contact_margin + y_offset),
                                         (x_offset + 200, 2*open_contact_margin + y_offset),
                                         (x_offset + 200, -10 + y_offset),
                                         (x_offset, -10 + y_offset)],
                                          layer=layer_data['contact_pads']['layer'], datatype=layer_data['contact_pads']['datatype'])
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, remove_right_margin, 'not',
                                     layer=layer_data['contact_pads']['layer'],
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
                                     layer=layer_data['contact_pads']['layer'],
                                     datatype=layer_data['contact_pads']['datatype'])
    
    
    square_side = 100
    square_x_offset = -50 + x_offset
    square_y_offset = -100 + y_offset
    
    square = gdstk.Polygon([(-square_side/2 + square_x_offset, -square_side/2 + square_y_offset),
                            ( square_side/2 + square_x_offset, -square_side/2 + square_y_offset),
                            ( square_side/2 + square_x_offset,  square_side/2 + square_y_offset),
                            (-square_side/2 + square_x_offset,  square_side/2 + square_y_offset)])
    
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, square, 'not',
                            layer=layer_data['contact_pads']['layer'],
                            datatype=layer_data['contact_pads']['datatype'])

    contact_pad_arch = contact_pad_arch[0]
    # polgygon_VCSEL.append(contact_pad_arch) 
    polgygon_VCSEL['contact_pad_arch'] = contact_pad_arch
    full_mask['contact_pads'].add(contact_pad_arch)
    
    
    
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
                                  layer=layer_data['contact_pads']['layer'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    # polgygon_VCSEL.append(taper_left)   
    polgygon_VCSEL['taper_left'] = taper_left
    full_mask['contact_pads'].add(taper_left)
    
    taper_right = gdstk.Polygon([(x_offset, y_offset),
                                (x_offset + 10, y_offset),
                                (contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset),
                                (-contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset)],
                                  layer=layer_data['contact_pads']['layer'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    cutout_radius = p_ring_inner + 1.5
    cutout_taper_right = create_circle(meas_x, meas_y, cutout_radius, layer_data['contact_pads'], circle_tolerance)
    
    taper_right = gdstk.boolean(taper_right, cutout_taper_right, 'not',
                            layer=layer_data['contact_pads']['layer'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    taper_right = taper_right[0]
    polgygon_VCSEL['taper_right'] = taper_right
    full_mask['contact_pads'].add(taper_right)
    
    ## EIGHTH LAYER: BOND PADS
    bond_pad_margin = 3
    
    bond_pad_left = gdstk.Polygon([(-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                      ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset, -contact_pad_side/2 + bond_pad_margin+ contact_pad_y_offset),
                                      ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset),
                                      (-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset)],
                                        layer=layer_data['bond_pads']['layer'], datatype=layer_data['bond_pads']['datatype'])
    
    polgygon_VCSEL['bond_pad_left'] = bond_pad_left
    full_mask['bond_pads'].add(bond_pad_left)
    
    
    
    bond_pad_right = gdstk.Polygon([(-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset + probe_length, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                       ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset + probe_length, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                       ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset + probe_length,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset),
                                       (-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset + probe_length,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset)],
                                        layer=layer_data['bond_pads']['layer'], datatype=layer_data['bond_pads']['datatype'])

    polgygon_VCSEL['bond_pad_right'] = bond_pad_right
    full_mask['bond_pads'].add(bond_pad_right)
    
    thickness = 5
    length    = 15
    MS_center_rect = 20
    
    MS_arm_offset = 50
    MS_arm_width  = 50
    MS_arm_height = 10
    
    
    
    x_offset_MS_align_top  = 125
    y_offset_MS_align_top  = 150
    
    if row == 0:

        x_MS_upper_left = x_offset - x_offset_MS_align_top
        y_MS_upper_left = y_offset + y_offset_MS_align_top
        
        
        create_MS_EBL_alignment(full_mask,
                                x_MS_upper_left, y_MS_upper_left,
                                MS_center_rect, MS_arm_offset,
                                MS_arm_width, MS_arm_height,
                                polgygon_VCSEL, 1,
                                layer_data)
        
        x_MS_upper_right = x_offset + x_offset_MS_align_top
        y_MS_upper_right = y_offset + y_offset_MS_align_top
        
        create_MS_EBL_alignment(full_mask,
                                x_MS_upper_right, y_MS_upper_right,
                                MS_center_rect, MS_arm_offset,
                                MS_arm_width, MS_arm_height,
                                polgygon_VCSEL, 2,
                                layer_data)
    
    
    x_offset_MS_align_bottom  = 125
    y_offset_MS_align_bottom  = 150
    
    x_MS_lower_left = x_offset - x_offset_MS_align_bottom
    y_MS_lower_left = y_offset - y_offset_MS_align_bottom
    
    
    create_MS_EBL_alignment(full_mask,
                            x_MS_lower_left, y_MS_lower_left,
                            MS_center_rect, MS_arm_offset,
                            MS_arm_width, MS_arm_height,
                            polgygon_VCSEL, 3,
                            layer_data)
    
    if not reverse_row:
        if column == 9:
            x_MS_lower_right = x_offset + x_offset_MS_align_bottom
            y_MS_lower_right = y_offset - y_offset_MS_align_bottom
            
            create_MS_EBL_alignment(full_mask,
                                    x_MS_lower_right, y_MS_lower_right,
                                    MS_center_rect, MS_arm_offset,
                                    MS_arm_width, MS_arm_height,
                                    polgygon_VCSEL, 4,
                                    layer_data)
    if reverse_row:
        if column == 0:
            x_MS_lower_right = x_offset + x_offset_MS_align_bottom
            y_MS_lower_right = y_offset - y_offset_MS_align_bottom
            
            create_MS_EBL_alignment(full_mask,
                                    x_MS_lower_right, y_MS_lower_right,
                                    MS_center_rect, MS_arm_offset,
                                    MS_arm_width, MS_arm_height,
                                    polgygon_VCSEL, 4,
                                    layer_data)
    
    
    return (polgygon_VCSEL, parameters_VCSEL)

def check_major_axis(major_axis_001, major, minor):
    if major_axis_001:
        return (major, minor)
    else: 
        return (minor, major)
        
def create_one_ellip_VCSEL(full_mask, layer_data,
                           x_offset, y_offset, 
                           p_ring_inner, p_ring_outer,
                           ellipticity, ellipticity_2, major_axis_001,
                           row, column, reverse_row,
                           n_contact_outer,
                           circle_tolerance):
    
    polgygon_VCSEL = {}
    parameters_VCSEL = {}
     
    ## GEOMETRY OF DIFFERENT OBJECTS
    p_ring_inner_major = p_ring_inner
    p_ring_inner_minor = ellipticity*p_ring_inner
    
    p_ring_inner = check_major_axis(major_axis_001, p_ring_inner_major, p_ring_inner_minor)
    
    
    p_ring_outer_major = p_ring_outer
    p_ring_outer_minor = ellipticity*p_ring_outer
    p_ring_outer = check_major_axis(major_axis_001, p_ring_outer_major, p_ring_outer_minor)
    
    
    ## FIRST LAYER: P RING
    p_ring_x = x_offset
    p_ring_y = y_offset
    
    # Create the geometry (a single rectangle) and add it to the cell.
    p_ring = create_annulus(p_ring_x, p_ring_y,
                            p_ring_inner, p_ring_outer,
                            layer_data['p_ring'], circle_tolerance)
    
    # polgygon_VCSEL.append(p_ring)
    polgygon_VCSEL['p_ring'] = p_ring
    full_mask['p_ring'].add(p_ring)
    
    
    # ## SECONDS LAYER: MESA PROTECTION
    mesa_radius_major = p_ring_outer_major + 2.0
    mesa_radius_minor = p_ring_outer_minor + 2.0
    mesa_radius = check_major_axis(major_axis_001, mesa_radius_major, mesa_radius_minor)
    
    meas_x      = x_offset
    meas_y      = y_offset
    
    mesa = create_circle(meas_x, meas_y, mesa_radius, layer_data['mesa'], circle_tolerance)
    
    polgygon_VCSEL['mesa'] = mesa
    full_mask['mesa'].add(mesa)
    parameters_VCSEL['mesa_diameter'] = 2*mesa_radius_major
    
    
    # ## THRID LAYER: OPEN SIDEWALLS FOR OXIDATION
    sidewall_inner_major  = mesa_radius_major - 4
    sidewall_inner_minor  = (1 + (1 - ellipticity_2))*(mesa_radius_minor - 4)
    
    sidewall_outer_major  = mesa_radius_major + 5.5
    sidewall_outer_minor  = mesa_radius_minor + 5.5
    
    sidewall_inner = check_major_axis(major_axis_001, sidewall_inner_major, sidewall_inner_minor)
    sidewall_outer = check_major_axis(major_axis_001, sidewall_outer_major, sidewall_outer_minor) 
    
    sidewall_x = x_offset
    sidewall_y = y_offset
    
    sidewall = create_annulus(sidewall_x, sidewall_y,
                              sidewall_inner, sidewall_outer,
                              layer_data['open_sidewalls'], circle_tolerance)
    
    # polgygon_VCSEL.append(sidewall)
    polgygon_VCSEL['sidewall'] = sidewall
    full_mask['open_sidewalls'].add(sidewall)
    
    
    
    # FOURTH LAYER: N CONTACTS
    # n_contact_thickness = 55
    distance_from_side_opening = 5
    
    n_contact_inner_major  = sidewall_outer_major + distance_from_side_opening
    n_contact_inner_minor  = ellipticity_2*n_contact_inner_major
    n_contact_inner_minor_for_contact  = ellipticity*n_contact_inner_major
    n_contact_inner = check_major_axis(major_axis_001, n_contact_inner_major, n_contact_inner_minor)
    
    n_contact_outer_major  = n_contact_outer#*(1 + (1-ellipticity)) #n_contact_inner + n_contact_thickness
    n_contact_outer_minor  = ellipticity*n_contact_outer
    n_contact_outer = check_major_axis(major_axis_001, n_contact_outer_major, n_contact_outer_minor)
    
    n_contact_x      = x_offset
    n_contact_y      = y_offset
    
    # CREATE ARCH
    n_contact = create_annulus(n_contact_x, n_contact_y,
                                n_contact_inner, n_contact_outer,
                                layer_data['n_ring'], circle_tolerance)
    
    
    # REMOVE TRIANGLE PART: BOOLEAN 'NOT'
    initial_angle_triangle = 0
    initial_angle_triangle_rad = initial_angle_triangle*np.pi/180
    
    final_angle_triangle  = 40
    final_angle_triangle_rad = final_angle_triangle*np.pi/180
    
    triangle_end_x = n_contact_outer_major + 500
    
    triangle_initial_end_y = triangle_end_x*np.tan(initial_angle_triangle_rad)
    triangle_final_end_y   = triangle_end_x*np.tan(final_angle_triangle_rad)
    
    triangle = gdstk.Polygon([(n_contact_x, n_contact_y),
                              (triangle_end_x + x_offset, -triangle_initial_end_y + y_offset),
                              (-triangle_end_x + x_offset, -triangle_final_end_y + y_offset)])
    
    n_contact = gdstk.boolean(n_contact, triangle, 'not',
                              layer=layer_data['n_ring']['layer'],
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
                            layer=layer_data['n_ring']['layer'],
                            datatype=layer_data['n_ring']['datatype'])
    n_contact = n_contact[0]
    
    # polgygon_VCSEL.append(n_contact)  
    polgygon_VCSEL['n_contact'] = n_contact
    full_mask['n_ring'].add(n_contact)
    
    
    
    ## SIXTH LAYER: OPEN CONTACTS
    ## CREATE ARCH FOR N CONTACTS
    ## THE SAME SETUP AS THE CONTACTS
    ## CREATE ANNULUS, REMOVE TRIANGLE AND SQUARE
    open_contact_margin = 2
        
    open_contacts_x = x_offset
    open_contacts_y = y_offset
    
    open_contacts_inner_major = n_contact_inner_major + open_contact_margin
    open_contacts_inner_minor = n_contact_inner_minor + open_contact_margin
    open_contacts_inner_minor_for_contact = n_contact_inner_minor_for_contact + open_contact_margin
    open_contacts_inner = check_major_axis(major_axis_001, open_contacts_inner_major, open_contacts_inner_minor)
    
    open_contacts_outer_major = n_contact_outer_major - open_contact_margin
    open_contacts_outer_minor = n_contact_outer_minor - open_contact_margin
    open_contacts_outer = check_major_axis(major_axis_001, open_contacts_outer_major, open_contacts_outer_minor)
    
    
    open_contact_arch = create_annulus(open_contacts_x, open_contacts_y,
                        open_contacts_inner, open_contacts_outer,
                        layer_data['n_ring'], circle_tolerance)

    
    # REMOVE TRIANGLE PART: BOOLEAN 'NOT'
    triangle_x_offset = 2 
    triangle_y_offset = open_contact_margin
    
    triangle = gdstk.Polygon([(n_contact_x - triangle_x_offset, n_contact_y + triangle_y_offset),
                              (triangle_end_x - triangle_x_offset + x_offset, -triangle_initial_end_y + triangle_y_offset + y_offset),
                              (-triangle_end_x - triangle_x_offset + x_offset, -triangle_final_end_y + triangle_y_offset + y_offset)])
    
    open_n_arch = gdstk.boolean(open_contact_arch, triangle, 'not', 
                            layer=layer_data['open_contacts']['layer'], 
                            datatype=layer_data['open_contacts']['datatype'])
    
    
    ## REMOVE SQUARE: BOOLEAN 'NOT'
    square_x_offset = square_x_offset
    square_y_offset = square_y_offset + open_contact_margin
    
    
    square = gdstk.Polygon([(-square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset, -square_side + square_y_offset),
                            ( square_side + square_x_offset,  square_side + square_y_offset),
                            (-square_side + square_x_offset,  square_side + square_y_offset)])
    
    open_n_arch = gdstk.boolean(open_n_arch, square, 'not',
                            layer=layer_data['open_contacts']['layer'],
                            datatype=layer_data['open_contacts']['datatype'])
    
    open_n_arch = open_n_arch[0]
    # polgygon_VCSEL.append(open_n_arch)    
    polgygon_VCSEL['open_n_arch'] = open_n_arch
    full_mask['open_contacts'].add(open_n_arch)
    
    
    ## CREATE CIRCLE FOR P CONTACT
    open_p_ring_margin   = 1.5
    open_p_contat_radius_major = p_ring_outer_major - open_p_ring_margin
    open_p_contat_radius_minor = (1 + (1 - ellipticity_2))*(p_ring_outer_minor - open_p_ring_margin)
    open_p_contat_radius = check_major_axis(major_axis_001, open_p_contat_radius_major, open_p_contat_radius_minor)
    
    open_p_contact = create_circle(open_contacts_x, open_contacts_y,
                        open_p_contat_radius, 
                        layer_data['open_contacts'], circle_tolerance)
    
    polgygon_VCSEL['open_p_contact'] = open_p_contact
    full_mask['open_contacts'].add(open_p_contact)
    
    
    ## SEVENTH LAYER: CONTACT PADS
    contact_pad_side = 70
    contact_pad_x_offset = -50 + x_offset
    contact_pad_y_offset = -100 + y_offset
    
    probe_length = 100
    
    contact_pad_left = gdstk.Polygon([(-contact_pad_side/2 + contact_pad_x_offset, -contact_pad_side/2 + contact_pad_y_offset),
                                      ( contact_pad_side/2 + contact_pad_x_offset, -contact_pad_side/2 + contact_pad_y_offset),
                                      ( contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset),
                                      (-contact_pad_side/2 + contact_pad_x_offset,  contact_pad_side/2 + contact_pad_y_offset)],
                                        layer=layer_data['contact_pads']['layer'], datatype=layer_data['contact_pads']['datatype'])
      
    polgygon_VCSEL['contact_pad_left'] = contact_pad_left
    full_mask['contact_pads'].add(contact_pad_left)
    
    
    contact_pad_right = gdstk.Polygon([(-contact_pad_side/2 + contact_pad_x_offset + probe_length, -contact_pad_side/2 + contact_pad_y_offset),
                                        ( contact_pad_side/2 + contact_pad_x_offset + probe_length, -contact_pad_side/2 + contact_pad_y_offset),
                                        ( contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset),
                                        (-contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset)],
                                        layer=layer_data['contact_pads']['layer'], datatype=layer_data['contact_pads']['datatype'])
 
    polgygon_VCSEL['contact_pad_right'] = contact_pad_right
    full_mask['contact_pads'].add(contact_pad_right)
    
    contact_pad_arch_inner_major  = n_contact_inner_major
    contact_pad_arch_inner_minor  = ellipticity*n_contact_inner_major
    contact_pad_arch_inner = check_major_axis(major_axis_001, contact_pad_arch_inner_major, contact_pad_arch_inner_minor)
    
    contact_pad_arch_outer_major  = n_contact_outer_major + 5
    contact_pad_arch_outer_minor  = ellipticity*contact_pad_arch_outer_major
    contact_pad_arch_outer = check_major_axis(major_axis_001, contact_pad_arch_outer_major, contact_pad_arch_outer_minor)
    
    contact_pad_x      = x_offset
    contact_pad_y      = y_offset
    
    contact_pad_arch = create_annulus(contact_pad_x, contact_pad_y,
                                      contact_pad_arch_inner, contact_pad_arch_outer,
                                      layer_data['contact_pads'], circle_tolerance)
    
    remove_arch_radius_major = contact_pad_arch_outer_major - 40
    remove_arch_radius_minor = ((ellipticity + ellipticity_2)/2)*remove_arch_radius_major
    remove_arch_radius = check_major_axis(major_axis_001, remove_arch_radius_major, remove_arch_radius_minor)
    
    
    remove_arch = create_circle(contact_pad_x, contact_pad_y,
                                remove_arch_radius, 
                                layer_data['contact_pads'], circle_tolerance)
    
    
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, remove_arch, 'not',
                            layer=layer_data['contact_pads']['layer'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    remove_right_margin = gdstk.Polygon([(x_offset, 2*open_contact_margin + y_offset),
                                          (x_offset + 200, 2*open_contact_margin + y_offset),
                                          (x_offset + 200, -10 + y_offset),
                                          (x_offset, -10 + y_offset)],
                                          layer=layer_data['contact_pads']['layer'], datatype=layer_data['contact_pads']['datatype'])
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, remove_right_margin, 'not',
                                      layer=layer_data['contact_pads']['layer'],
                                      datatype=layer_data['contact_pads']['datatype'])
    
    
    initial_angle_triangle = 0
    initial_angle_triangle_rad = initial_angle_triangle*np.pi/180
    
    final_angle_triangle  = 40
    final_angle_triangle_rad = final_angle_triangle*np.pi/180
    
    triangle_end_x = n_contact_outer_major + 500
    
    triangle_initial_end_y = triangle_end_x*np.tan(initial_angle_triangle_rad)
    triangle_final_end_y   = triangle_end_x*np.tan(final_angle_triangle_rad)
    
    
    triangle = gdstk.Polygon([(n_contact_x, n_contact_y),
                              (triangle_end_x + x_offset, -triangle_initial_end_y + y_offset),
                              (-triangle_end_x + x_offset, -triangle_final_end_y + y_offset)])

    contact_pad_arch = gdstk.boolean(contact_pad_arch, triangle, 'not',
                                     layer=layer_data['contact_pads']['layer'],
                                     datatype=layer_data['contact_pads']['datatype'])
    
    
    square_side = 100
    square_x_offset = -50 + x_offset
    square_y_offset = -100 + y_offset
    
    square = gdstk.Polygon([(-square_side/2 + square_x_offset, -square_side/2 + square_y_offset),
                            ( square_side/2 + square_x_offset, -square_side/2 + square_y_offset),
                            ( square_side/2 + square_x_offset,  square_side/2 + square_y_offset),
                            (-square_side/2 + square_x_offset,  square_side/2 + square_y_offset)])
    
    
    contact_pad_arch = gdstk.boolean(contact_pad_arch, square, 'not',
                                     layer=layer_data['contact_pads']['layer'],
                                     datatype=layer_data['contact_pads']['datatype'])

    contact_pad_arch = contact_pad_arch[0]
    # polgygon_VCSEL.append(contact_pad_arch) 
    polgygon_VCSEL['contact_pad_arch'] = contact_pad_arch
    full_mask['contact_pads'].add(contact_pad_arch)
    
    
    
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
                                  layer=layer_data['contact_pads']['layer'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    # polgygon_VCSEL.append(taper_left)   
    polgygon_VCSEL['taper_left'] = taper_left
    full_mask['contact_pads'].add(taper_left)
    
    taper_right = gdstk.Polygon([(x_offset, y_offset),
                                (x_offset + 10, y_offset),
                                (contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset),
                                (-contact_pad_side/2 + contact_pad_x_offset + probe_length,  contact_pad_side/2 + contact_pad_y_offset)],
                                  layer=layer_data['contact_pads']['layer'],
                                  datatype=layer_data['contact_pads']['datatype'])
    
    
    

    cutout_radius_major = p_ring_inner_major + 1.5
    cutout_radius_minor = ellipticity*(p_ring_inner_major + 1.5)
    
    cutout_radius = check_major_axis(major_axis_001, cutout_radius_major, cutout_radius_minor)
    
    cutout_taper_right = create_circle(meas_x, meas_y, 
                                       cutout_radius, 
                                       layer_data['contact_pads'], circle_tolerance)
    
    taper_right = gdstk.boolean(taper_right, cutout_taper_right, 'not',
                            layer=layer_data['contact_pads']['layer'],
                            datatype=layer_data['contact_pads']['datatype'])
    
    taper_right = taper_right[0]
    polgygon_VCSEL['taper_right'] = taper_right
    full_mask['contact_pads'].add(taper_right)
    
    ## EIGHTH LAYER: BOND PADS
    bond_pad_margin = 3
    
    bond_pad_left = gdstk.Polygon([(-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                   ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset, -contact_pad_side/2 + bond_pad_margin+ contact_pad_y_offset),
                                   ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset),
                                   (-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset)],
                                     layer=layer_data['bond_pads']['layer'], datatype=layer_data['bond_pads']['datatype'])
    
    polgygon_VCSEL['bond_pad_left'] = bond_pad_left
    full_mask['bond_pads'].add(bond_pad_left)
    
    
    
    bond_pad_right = gdstk.Polygon([(-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset + probe_length, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                        ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset + probe_length, -contact_pad_side/2 + bond_pad_margin + contact_pad_y_offset),
                                        ( contact_pad_side/2 - bond_pad_margin + contact_pad_x_offset + probe_length,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset),
                                        (-contact_pad_side/2 + bond_pad_margin + contact_pad_x_offset + probe_length,  contact_pad_side/2 - bond_pad_margin + contact_pad_y_offset)],
                                        layer=layer_data['bond_pads']['layer'], datatype=layer_data['bond_pads']['datatype'])

    polgygon_VCSEL['bond_pad_right'] = bond_pad_right
    full_mask['bond_pads'].add(bond_pad_right)
    
    thickness = 5
    length    = 15
    MS_center_rect = 20
    
    MS_arm_offset = 50
    MS_arm_width  = 50
    MS_arm_height = 10
    
    
    
    x_offset_MS_align_top  = 125
    y_offset_MS_align_top  = 150
    
    if row == 0:

        x_MS_upper_left = x_offset - x_offset_MS_align_top
        y_MS_upper_left = y_offset + y_offset_MS_align_top
        
        
        create_MS_EBL_alignment(full_mask,
                                x_MS_upper_left, y_MS_upper_left,
                                MS_center_rect, MS_arm_offset,
                                MS_arm_width, MS_arm_height,
                                polgygon_VCSEL, 1,
                                layer_data)
        
        x_MS_upper_right = x_offset + x_offset_MS_align_top
        y_MS_upper_right = y_offset + y_offset_MS_align_top
        
        create_MS_EBL_alignment(full_mask,
                                x_MS_upper_right, y_MS_upper_right,
                                MS_center_rect, MS_arm_offset,
                                MS_arm_width, MS_arm_height,
                                polgygon_VCSEL, 2,
                                layer_data)
    
    
    x_offset_MS_align_bottom  = 125
    y_offset_MS_align_bottom  = 150
    
    x_MS_lower_left = x_offset - x_offset_MS_align_bottom
    y_MS_lower_left = y_offset - y_offset_MS_align_bottom
    
    
    create_MS_EBL_alignment(full_mask,
                            x_MS_lower_left, y_MS_lower_left,
                            MS_center_rect, MS_arm_offset,
                            MS_arm_width, MS_arm_height,
                            polgygon_VCSEL, 3,
                            layer_data)
    
    if not reverse_row:
        if column == 9:
            x_MS_lower_right = x_offset + x_offset_MS_align_bottom
            y_MS_lower_right = y_offset - y_offset_MS_align_bottom
            
            create_MS_EBL_alignment(full_mask,
                                    x_MS_lower_right, y_MS_lower_right,
                                    MS_center_rect, MS_arm_offset,
                                    MS_arm_width, MS_arm_height,
                                    polgygon_VCSEL, 4,
                                    layer_data)
    if reverse_row:
        if column == 0:
            x_MS_lower_right = x_offset + x_offset_MS_align_bottom
            y_MS_lower_right = y_offset - y_offset_MS_align_bottom
            
            create_MS_EBL_alignment(full_mask,
                                    x_MS_lower_right, y_MS_lower_right,
                                    MS_center_rect, MS_arm_offset,
                                    MS_arm_width, MS_arm_height,
                                    polgygon_VCSEL, 4,
                                    layer_data)
    
    
    return (polgygon_VCSEL, parameters_VCSEL)

def main():
    ## SETUP VARIABLES ##
    # File to save mask
    mask_folder = 'MASKS/'
        
    if not os.path.exists(mask_folder):
        os.makedirs(mask_folder)
    
    mask_name   = 'KAW_BE_v1'
    
    # Name of cell
    cell_name   = 'KAW_BE_v1'
    
    save_layout = True
    
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
    
    
    # Number for each layer in VCSEL
    p_ring_layer         = 1
    mesa_layer           = 2
    open_sidewalls_layer = 3
    witness_mesa_layer   = 4
    n_ring_layer         = 5
    open_contacts_layer  = 6
    contact_pad_layer    = 7
    bond_pad_layer       = 8
    MS_a_marks_layer     = 9
    
    CF_frame_layer       = 10
    DF_frame_layer       = 11
    
    entire_chip_layer    = 12
    
    layer_data = {
        'p_ring': {'layer': p_ring_layer, 'datatype': 1},
        'mesa': {'layer': mesa_layer, 'datatype': 1},
        'open_sidewalls': {'layer': open_sidewalls_layer, 'datatype': 1},
        'witness_mesa' : {'layer': witness_mesa_layer, 'datatype': 1},
        'n_ring': {'layer': n_ring_layer, 'datatype': 1},
        'open_contacts': {'layer': open_contacts_layer, 'datatype': 1},
        'contact_pads': {'layer': contact_pad_layer, 'datatype': 1},
        'bond_pads': {'layer': bond_pad_layer, 'datatype': 1},
        'MS_align': {'layer': MS_a_marks_layer, 'datatype': 1},
        'CF_frame': {'layer': CF_frame_layer, 'datatype': 1},
        'DF_frame': {'layer': DF_frame_layer, 'datatype': 1},
        'entire_chip' : {'layer': entire_chip_layer, 'datatype': 1}
    }
    
    layer_data_reversed = {}    
    for k, v in layer_data.items():
        layer_data_reversed[v['layer']] = k
        
    full_mask = {}
    
    for layer in layer_data.keys():
        full_mask[layer] = lib.new_cell(layer)
    
    ##### ADD EVERYTHING THAT IS NOT A VCSEL
    ## PARAMETERS FOR ENTIRE CHIP
    chip_center_x = 0
    chip_center_y = 0
    
    chip_size_x = 8000
    chip_size_y = 10000
    
    entire_chip = create_rectangle(chip_center_x, chip_center_y, chip_size_x, chip_size_y, layer_data['entire_chip'])
    # mask.add(entire_chip)
    full_mask['entire_chip'].add(entire_chip)
    
    
    
    ## FRAMES
    frame_marginal = 2000
    
    frame_size_x = chip_size_x - frame_marginal
    frame_size_y = chip_size_y - frame_marginal
    
    CF_frame = create_rectangle(chip_center_x, chip_center_y, frame_size_x, frame_size_y, layer_data['CF_frame'])
    # mask.add(CF_frame)
    # full_mask['CF_frame'] = CF_frame
    full_mask['CF_frame'].add(CF_frame)
    
    DF_frame = create_rectangle(chip_center_x, chip_center_y, frame_size_x, frame_size_y, layer_data['DF_frame'])
    # mask.add(DF_frame)
    full_mask['DF_frame'].add(DF_frame)
    
    ####### ALIGNMENT MARKS ###############
    
    ## CREATING THE A MARKS ON THE P CONTACT LAYER ### FIRST LAYER
    row_number = 4
    a_mark_x_offset = 500
    a_mark_y_offset = 500
    
    frame_margin_default  = 250
    frame_margin_x    = frame_margin_default + 0
    frame_margin_y    = frame_margin_default + 0
    
    alignment_marks = create_all_alignement_marks(frame_size_x, frame_size_y,
                                                  row_number,
                                                  a_mark_x_offset, a_mark_y_offset,
                                                  frame_margin_x, frame_margin_y,
                                                  layer_data['p_ring'])
    
    # mask.add(*alignment_marks)
    full_mask['p_ring'].add(*alignment_marks)
    
    ## ALIGNMENT MARKS FOR MESA ### SECOND LAYER
    upper_mesa_cover = cover_upper_mesa(chip_center_x, chip_center_y,
                                        frame_size_x, frame_size_y,
                                        a_mark_x_offset, a_mark_y_offset,
                                        frame_margin_default,
                                        frame_margin_x, frame_margin_y,
                                        layer_data['mesa'])
    # mask.add(upper_mesa_cover)
    full_mask['mesa'].add(upper_mesa_cover)
        
    lower_mesa_cover = cover_lower_mesa(chip_center_x, chip_center_y,
                                        frame_size_x, frame_size_y,
                                        row_number,
                                        a_mark_x_offset, a_mark_y_offset,
                                        frame_margin_default,
                                        frame_margin_x, frame_margin_y,
                                        layer_data['mesa'])
    # mask.add(*lower_mesa_cover)
    full_mask['mesa'].add(*lower_mesa_cover)

    
    all_a_marks = create_all_a_mark_mesa(frame_size_x, frame_size_y,
                                         frame_margin_x, frame_margin_y,
                                         a_mark_x_offset, a_mark_y_offset,
                                         layer_data)
    
    # mask.add(*all_a_marks)
    full_mask['mesa'].add(*all_a_marks)
    
    
    ## ALIGNMENT MARKS FOR OPEN SIDE WALLS ### THIRD LAYER
    a_mark_open_sidewall = create_all_a_mark_open_sidewall(frame_size_x, frame_size_y,
                                                           a_mark_x_offset, a_mark_y_offset,
                                                           layer_data['open_sidewalls'])
    
    # mask.add(*a_mark_open_sidewall)
    full_mask['open_sidewalls'].add(*a_mark_open_sidewall)

    ## COVER ENTIRE SIDES FOR OPEN SIDE WALLS
    cover_sides_open_sidewalls = create_side_cover(chip_center_x, chip_center_y,
                                                   chip_size_x, chip_size_y,
                                                   frame_size_x, frame_size_y,
                                                   layer_data['open_sidewalls'])
    
    # mask.add(*cover_sides_open_sidewalls)
    full_mask['open_sidewalls'].add(*cover_sides_open_sidewalls)
    
    ## ALIGENMENT MARKS FOR WITNESS MESA ETCH  ### FOURTH LAYER
    a_mark_witness_mesa = create_all_a_mark_witness_mesa(frame_size_x, frame_size_y,
                                                            a_mark_x_offset, a_mark_y_offset,
                                                            layer_data['witness_mesa'])
    
    # mask.add(*a_mark_witness_mesa)
    full_mask['witness_mesa'].add(*a_mark_witness_mesa)
    
    ## COVER ENTIRE SIDES FOR BOTTOM CONTACT
    cover_sides_witness_mesa = create_side_cover(chip_center_x, chip_center_y,
                                                   chip_size_x, chip_size_y,
                                                   frame_size_x, frame_size_y,
                                                   layer_data['witness_mesa'])
    
    # mask.add(*cover_sides_witness_mesa)
    full_mask['witness_mesa'].add(*cover_sides_witness_mesa)
    
    
    
    ## ALIGENMENT MARKS FOR BOTTOM CONTACT ### FIFTH LAYER
    a_mark_bottom_contact = create_all_a_mark_bottom_contact(frame_size_x, frame_size_y,
                                                           a_mark_x_offset, a_mark_y_offset,
                                                           layer_data['n_ring'])
    
    # mask.add(*a_mark_bottom_contact)
    full_mask['n_ring'].add(*a_mark_bottom_contact)
    
    ## COVER ENTIRE SIDES FOR BOTTOM CONTACT
    cover_sides_bottom_contact = create_side_cover(chip_center_x, chip_center_y,
                                                   chip_size_x, chip_size_y,
                                                   frame_size_x, frame_size_y,
                                                   layer_data['n_ring'])
    
    # mask.add(*cover_sides_bottom_contact)
    full_mask['n_ring'].add(*cover_sides_bottom_contact)
    
    ## COVER FOR OPEN CONTACTS ### SIXTH LAYER
    open_contacts_cover_upper = cover_upper_open_contacts(chip_center_x, chip_center_y,
                                                          frame_size_x, frame_size_y,
                                                          a_mark_x_offset, a_mark_y_offset,
                                                          frame_margin_default,
                                                          frame_margin_x, frame_margin_y,
                                                          layer_data['open_contacts'])
    # mask.add(*open_contacts_cover_upper)
    full_mask['open_contacts'].add(*open_contacts_cover_upper)
    
    
    open_contacts_cover_lower =  cover_lower_open_contacts(chip_center_x, chip_center_y,
                                                            frame_size_x, frame_size_y,
                                                            row_number,
                                                            a_mark_x_offset, a_mark_y_offset,
                                                            frame_margin_default,
                                                            frame_margin_x, frame_margin_y,
                                                            layer_data['open_contacts'])
    # mask.add(*open_contacts_cover_lower)
    full_mask['open_contacts'].add(*open_contacts_cover_lower)
    
    ## ALIGENMENT MARKS FOR CONTACT PADS ### SEVENTH LAYER
    left_mark_x = -frame_size_x/2 + a_mark_x_offset/2 + 2*a_mark_x_offset
    left_mark_y = frame_size_y/2  - a_mark_y_offset/2 
    
    left_upper_a_mark_contact_pads = create_cover_DF_a_mark(left_mark_x, left_mark_y,
                                                a_mark_x_offset, a_mark_y_offset, 
                                                layer_data['contact_pads'])
    
    # mask.add(*left_upper_a_mark_contact_pads)
    full_mask['contact_pads'].add(*left_upper_a_mark_contact_pads)
    
    
    left_upper_a_mark_contact_pads_rotated = create_cover_DF_a_mark(left_mark_x, left_mark_y,
                                             a_mark_x_offset, a_mark_y_offset, 
                                             layer_data['contact_pads'])
    

    for i in left_upper_a_mark_contact_pads_rotated:
        i.rotate(np.pi)
    
    # mask.add(*left_upper_a_mark_contact_pads_rotated)
    full_mask['contact_pads'].add(*left_upper_a_mark_contact_pads_rotated)
    
    right_mark_x = frame_size_x/2 - a_mark_x_offset/2 - 2*a_mark_x_offset
    right_mark_y = frame_size_y/2  - a_mark_y_offset/2
    right_upper_a_mark_contact_pads = create_cover_DF_a_mark(right_mark_x, right_mark_y,
                                             a_mark_x_offset, a_mark_y_offset, 
                                             layer_data['contact_pads'])
    
    # mask.add(*right_upper_a_mark_contact_pads)
    full_mask['contact_pads'].add(*right_upper_a_mark_contact_pads)
    
    right_a_mark_contact_pads_rotated = create_cover_DF_a_mark(right_mark_x, right_mark_y,
                                             a_mark_x_offset, a_mark_y_offset, 
                                             layer_data['contact_pads'])
    
    for i in right_a_mark_contact_pads_rotated:
        i.rotate(np.pi)

    
    # mask.add(*right_a_mark_contact_pads_rotated)
    full_mask['contact_pads'].add(*right_a_mark_contact_pads_rotated)
    
    
    cover_sides_contact_pads = create_side_cover(chip_center_x, chip_center_y,
                                               chip_size_x, chip_size_y,
                                               frame_size_x, frame_size_y,
                                               layer_data['contact_pads'])
    
    # mask.add(*cover_sides_contact_pads)
    full_mask['contact_pads'].add(*cover_sides_contact_pads)
    
    ## ALIGNMENT MARKS FOR BONDPADS ### EIGTH LAYER
    left_mark_x = -frame_size_x/2 + a_mark_x_offset/2 + 3*a_mark_x_offset
    left_mark_y = frame_size_y/2  - a_mark_y_offset/2
    
    left_upper_a_mark_bond_pads = create_cover_DF_a_mark(left_mark_x, left_mark_y,
                                                            a_mark_x_offset, a_mark_y_offset, 
                                                            layer_data['bond_pads'])
    
    # mask.add(*left_upper_a_mark_bond_pads)
    full_mask['bond_pads'].add(*left_upper_a_mark_bond_pads)
    
    
    left_upper_a_mark_bond_pads_rotated = create_cover_DF_a_mark(left_mark_x, left_mark_y,
                                                                 a_mark_x_offset, a_mark_y_offset, 
                                                                 layer_data['bond_pads'])
    

    for i in left_upper_a_mark_bond_pads_rotated:
        i.rotate(np.pi)
    
    # mask.add(*left_upper_a_mark_bond_pads_rotated)
    full_mask['bond_pads'].add(*left_upper_a_mark_bond_pads_rotated)
    
    right_mark_x = frame_size_x/2 - a_mark_x_offset/2 - 3*a_mark_x_offset
    right_mark_y = frame_size_y/2  - a_mark_y_offset/2 
    right_upper_a_mark_bond_pads = create_cover_DF_a_mark(right_mark_x, right_mark_y,
                                              a_mark_x_offset, a_mark_y_offset, 
                                              layer_data['bond_pads'])
    
    # mask.add(*right_upper_a_mark_bond_pads)
    full_mask['bond_pads'].add(*right_upper_a_mark_bond_pads)
    
    right_a_mark_bond_pads_rotated = create_cover_DF_a_mark(right_mark_x, right_mark_y,
                                              a_mark_x_offset, a_mark_y_offset, 
                                              layer_data['bond_pads'])
    
    for i in right_a_mark_bond_pads_rotated:
        i.rotate(np.pi)

    
    # mask.add(*right_a_mark_bond_pads_rotated)
    full_mask['bond_pads'].add(*right_a_mark_bond_pads_rotated)
    
    
    cover_sides_bond_pads = create_side_cover(chip_center_x, chip_center_y,
                                                chip_size_x, chip_size_y,
                                                frame_size_x, frame_size_y,
                                                layer_data['bond_pads'])
    
    # mask.add(*cover_sides_bond_pads)
    full_mask['bond_pads'].add(*cover_sides_bond_pads)
    
    ## ALIGNMENT MARKS FOR BACKSIDE METASURFACE
    # cover_upper_MS_align = cover_upper_MS_alignment(chip_center_x, chip_center_y,
    #                                                frame_size_x, frame_size_y,
    #                                                a_mark_x_offset, a_mark_y_offset,
    #                                                frame_margin_default,
    #                                                frame_margin_x, frame_margin_y,
    #                                                layer_data['MS_align'])
    

    # mask.add(*cover_upper_MS_align)
    
    # cover_lower_MS_align = cover_lower_MS_alignment(chip_center_x, chip_center_y,
    #                                                 frame_size_x, frame_size_y,
    #                                                 row_number,
    #                                                 a_mark_x_offset, a_mark_y_offset,
    #                                                 frame_margin_default,
    #                                                 frame_margin_x, frame_margin_y,
    #                                                 layer_data['MS_align'])
    
    # mask.add(*cover_lower_MS_align)
    
    # all_a_marks_MS_align = create_all_a_mark_MS_align(frame_size_x, frame_size_y,
    #                                                   frame_margin_x, frame_margin_y,
    #                                                   a_mark_x_offset, a_mark_y_offset,
    #                                                   layer_data)
    
    # # mask.add(*all_a_marks_MS_align)
    # # full_mask['MS_align'].add(*all_a_marks_MS_align)
    
    MS_center_rect = 20
    MS_arm_offset  = 280
    
    MS_arm_width   = 320
    MS_arm_height  = 10
    
    x_MS_upper_left = -frame_size_x/2 + 2*a_mark_x_offset
    y_MS_upper_left =  frame_size_y/2 - a_mark_y_offset

    
    create_combo_mark(full_mask,
                      x_MS_upper_left, y_MS_upper_left,
                      MS_center_rect, MS_arm_offset,
                      MS_arm_width, MS_arm_height,
                      1,
                      layer_data)
    
    all_a_marks_MS_align = create_all_a_mark_MS_align(frame_size_x, frame_size_y,
                                                      frame_margin_x, frame_margin_y,
                                                      a_mark_x_offset, a_mark_y_offset,
                                                      layer_data)
    
    x_MS_upper_right = frame_size_x/2 - 2*a_mark_x_offset
    y_MS_upper_right =  frame_size_y/2 - a_mark_y_offset

    
    create_combo_mark(full_mask,
                      x_MS_upper_right, y_MS_upper_right,
                      MS_center_rect, MS_arm_offset,
                      MS_arm_width, MS_arm_height,
                      1,
                      layer_data)
    
    all_a_marks_MS_align = create_all_a_mark_MS_align(frame_size_x, frame_size_y,
                                                      frame_margin_x, frame_margin_y,
                                                      a_mark_x_offset, a_mark_y_offset,
                                                      layer_data)
    
    x_MS_lower_left = -frame_size_x/2 + 2*a_mark_x_offset
    y_MS_lower_left = -frame_size_y/2 + a_mark_y_offset

    
    create_combo_mark(full_mask,
                      x_MS_lower_left, y_MS_lower_left,
                      MS_center_rect, MS_arm_offset,
                      MS_arm_width, MS_arm_height,
                      1,
                      layer_data)
    
    all_a_marks_MS_align = create_all_a_mark_MS_align(frame_size_x, frame_size_y,
                                                      frame_margin_x, frame_margin_y,
                                                      a_mark_x_offset, a_mark_y_offset,
                                                      layer_data)
    
    x_MS_lower_right = frame_size_x/2 - 2*a_mark_x_offset
    y_MS_lower_right = -frame_size_y/2 + a_mark_y_offset

    
    create_combo_mark(full_mask,
                      x_MS_lower_right, y_MS_lower_right,
                      MS_center_rect, MS_arm_offset,
                      MS_arm_width, MS_arm_height,
                      1,
                      layer_data)
    
    all_a_marks_MS_align = create_all_a_mark_MS_align(frame_size_x, frame_size_y,
                                                      frame_margin_x, frame_margin_y,
                                                      a_mark_x_offset, a_mark_y_offset,
                                                      layer_data)
    
    
    
    
    # mask.add(*all_a_marks_MS_align)
    full_mask['MS_align'].add(*all_a_marks_MS_align)
    
    thickness = 8
    length    = 200
    ms_align_to_top_mesa = create_one_a_mark(-frame_size_x/2 + a_mark_x_offset/2, frame_size_y/2 - a_mark_y_offset/2 - a_mark_y_offset, 
                                             thickness, length, 
                                             layer_data['MS_align'])
    
    full_mask['MS_align'].add(*ms_align_to_top_mesa)
    
    ms_align_to_top_mesa = create_one_a_mark(frame_size_x/2 - a_mark_x_offset/2, frame_size_y/2 - a_mark_y_offset/2 - a_mark_y_offset, 
                                             thickness, length, 
                                             layer_data['MS_align'])
    
    full_mask['MS_align'].add(*ms_align_to_top_mesa)
    
    ms_align_to_top_mesa = create_one_a_mark(-frame_size_x/2 + a_mark_x_offset/2, -frame_size_y/2 + a_mark_y_offset/2 + a_mark_y_offset, 
                                             thickness, length, 
                                             layer_data['MS_align'])
    
    full_mask['MS_align'].add(*ms_align_to_top_mesa)
    
    ms_align_to_top_mesa = create_one_a_mark(frame_size_x/2 - a_mark_x_offset/2, -frame_size_y/2 + a_mark_y_offset/2 + a_mark_y_offset, 
                                             thickness, length, 
                                             layer_data['MS_align'])
    
    full_mask['MS_align'].add(*ms_align_to_top_mesa)
    
    
    ####### ARROW FOR ORIENTATION #######
    arrow_head          = 400
    arrow_base          = 500
    arrow_margin        = 50
    orientation_arrow_x = 0
    orientation_arrow_y = frame_size_y/2 - arrow_head - arrow_margin
    
    orientation_arrow = create_orientation_arrow(orientation_arrow_x, orientation_arrow_y,
                                                 arrow_head, arrow_base,
                                                 layer_data['p_ring'])
    # mask.add(orientation_arrow)
    full_mask['p_ring'].add(orientation_arrow)
        
        
    ## TLM PADS
    # CIRCLES FOR P CONTACTS
    left_circles_x = 1875
    left_circles_y = 50
    TLM_circles = create_TLM_p_circles(-left_circles_x, left_circles_y, layer_data, circle_tolerance)
    
    # mask.add(*TLM_circles)    
    add_list_to_layer(TLM_circles, full_mask, layer_data_reversed)
    
    lower_circles_x = -400
    lower_circles_y = -3300
    TLM_circles = create_TLM_p_circles(lower_circles_x, lower_circles_y, layer_data, circle_tolerance)
    
    #mask.add(*TLM_circles)
    add_list_to_layer(TLM_circles, full_mask, layer_data_reversed)
    
    # CIRCLES FOR N CONTACTS
    TLM_circles = create_TLM_n_circles(left_circles_x, left_circles_y, layer_data, circle_tolerance)
    
    #mask.add(*TLM_circles)
    add_list_to_layer(TLM_circles, full_mask, layer_data_reversed)
    
    lower_circles_x = -400
    lower_circles_y = -3800
    TLM_circles = create_TLM_n_circles(lower_circles_x, lower_circles_y, layer_data, circle_tolerance)
    
    #mask.add(*TLM_circles)
    add_list_to_layer(TLM_circles, full_mask, layer_data_reversed)
    
    ## RECTANGLES
    # PADS FOR P CONTACTS
    pads_right_x = 665
    pads_right_y = 50
    TLM_pads_right = TLM_p_pads(-pads_right_x, pads_right_y, layer_data)
    
    #mask.add(*TLM_pads_right)
    add_list_to_layer(TLM_pads_right, full_mask, layer_data_reversed)
    
    pads_lower_x = -200
    pads_lower_y = -3100
    TLM_pads_lower = TLM_p_pads(pads_lower_x, pads_lower_y, layer_data)
    
    # mask.add(*TLM_pads_lower)
    add_list_to_layer(TLM_pads_lower, full_mask, layer_data_reversed)
    
    
    # PADS FOR N CONTACTS
    TLM_pads_right = TLM_n_pads(pads_right_x+435, pads_right_y, layer_data)
   
    # mask.add(*TLM_pads_right)
    add_list_to_layer(TLM_pads_right, full_mask, layer_data_reversed)
    
    lower_pads_y = -3600
    TLM_pads_lower = TLM_n_pads(pads_lower_x, lower_pads_y, layer_data)
    
    # mask.add(*TLM_pads_lower)
    add_list_to_layer(TLM_pads_lower, full_mask, layer_data_reversed)
    
    
    #### ADD VCSELS #############
    # Try to add elements to the defined mask
    #try:
    # create mask
    # x = np.arange(0, 2000, 250)
    # for i in x:
    #     for j in x:
    #         create_one_VCSEL(mask, layer_data, i, j, 5, 10)
    
    n_contact_outer = 80
    # create_one_VCSEL(mask, layer_data, -frame_size_x/2 + 350,  frame_size_y/2 - 1200, 4, 9, n_contact_outer)   # OXIDE 1UM
    
    
    diff_row = 300
    
    number_of_rows = 9
    number_of_colums = 10
    
    
    p_ring_outer_1 = np.array([7.75, 8.75, 9.25, 9.5, 9.75, 10.0, 10.25, 10.50, 11.00])
    p_ring_outer_2 = np.array([8.00, 9.00, 9.25, 9.5, 9.75, 10.0, 10.25, 10.75, 11.25])
    
    p_ring_inner_1 = p_ring_outer_1 - 4.5
    p_ring_inner_2 = p_ring_outer_2 - 4.5
    
    
    ## RESULTING MESA SIZES
    mesa_size = 2*(p_ring_outer_1 + 2)
 #   print(mesa_size)

    
    for i in range(number_of_rows):
        
        VCSEL_y = frame_size_y/2 - 1200 - i*diff_row
        
        open_mesa_width  = 60
        open_mesa_height = 100
        
        mesa_etch_margin = 4
        mesa_etch_width  = open_mesa_width + mesa_etch_margin
        mesa_etch_height = open_mesa_height + mesa_etch_margin
        
        for j in range(number_of_colums):
            VCSEL_x = -frame_size_x/2 + 350 + j*250
            
            reverse_row = False
            
            if j < 5:
                VCSEL, VCSEL_parameters = create_one_VCSEL(full_mask, layer_data,
                                                           VCSEL_x, VCSEL_y,
                                                           p_ring_inner_1[i], p_ring_outer_1[i],
                                                           i, j,
                                                           reverse_row,
                                                           n_contact_outer, circle_tolerance)
            else:
                VCSEL, VCSEL_parameters = create_one_VCSEL(full_mask, layer_data,
                                                           VCSEL_x, VCSEL_y,
                                                           p_ring_inner_2[i], p_ring_outer_2[i],
                                                           i, j,
                                                           reverse_row,
                                                           n_contact_outer, circle_tolerance)
            
            mesa_diameter = VCSEL_parameters['mesa_diameter']
            mesa_radius   = mesa_diameter/2
            mesa_diameter_string = str(math.floor(mesa_diameter))
            
            if j == 0:
                
                left_offset = -250
                witness_mesa_left_x = VCSEL_x + left_offset
                witness_mesa_left = create_circle(witness_mesa_left_x, VCSEL_y, mesa_radius, layer_data['mesa'], circle_tolerance)
                # mask.add(witness_mesa_left)
                full_mask['mesa'].add(witness_mesa_left)
                
                
                left_text_x = VCSEL_x + left_offset - 21
                left_text_y = VCSEL_y + 10
                top_mesa_label = create_mesa_label(left_text_x, left_text_y, mesa_diameter_string, layer_data['mesa'])
                # mask.add(*top_mesa_label)
                add_list_to_layer(top_mesa_label, full_mask, layer_data_reversed)
                
                open_witeness_mesa = create_rectangle(witness_mesa_left_x, VCSEL_y,
                                                      open_mesa_width, open_mesa_height, 
                                                      layer_data['open_sidewalls'])
                # mask.add(open_witeness_mesa)
                full_mask['open_sidewalls'].add(open_witeness_mesa)
                
                
                
                witeness_mesa_etch = create_rectangle(witness_mesa_left_x, VCSEL_y,
                                                      mesa_etch_width, mesa_etch_height, 
                                                      layer_data['witness_mesa'])
                # mask.add(witeness_mesa_etch)
                full_mask['witness_mesa'].add(witeness_mesa_etch)
                
                
                
                open_etch_witeness_mesa = create_rectangle(witness_mesa_left_x, VCSEL_y,
                                                      open_mesa_width, open_mesa_height, 
                                                      layer_data['open_contacts'])
                # mask.add(open_etch_witeness_mesa)
                full_mask['open_contacts'].add(open_etch_witeness_mesa)
                
                
                
            
            if j == 9:
                
                right_offset = 400
                witness_mesa_right_x = VCSEL_x + right_offset
                witness_mesa_right = create_circle(witness_mesa_right_x, VCSEL_y, mesa_radius, layer_data['mesa'], circle_tolerance)
                # mask.add(witness_mesa_right)
                full_mask['mesa'].add(witness_mesa_right)
                
                right_text_x = VCSEL_x + right_offset - 21
                right_text_y = VCSEL_y + 10
                top_mesa_label = create_mesa_label(right_text_x, right_text_y, mesa_diameter_string, layer_data['mesa'])
                # mask.add(*top_mesa_label)
                add_list_to_layer(top_mesa_label, full_mask, layer_data_reversed)
                
                open_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                      open_mesa_width, open_mesa_height, 
                                                      layer_data['open_sidewalls'])
                # mask.add(open_witeness_mesa)
                full_mask['open_sidewalls'].add(open_witeness_mesa)
                
                witeness_mesa_etch = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                      mesa_etch_width, mesa_etch_height, 
                                                      layer_data['witness_mesa'])
                # mask.add(witeness_mesa_etch)
                full_mask['witness_mesa'].add(witeness_mesa_etch)
                
                
                open_etch_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                      open_mesa_width, open_mesa_height, 
                                                      layer_data['open_contacts'])
                # mask.add(open_etch_witeness_mesa)
                full_mask['open_contacts'].add(open_etch_witeness_mesa)
                
        
            for j in range(10):
                VCSEL_x = frame_size_x/2 - 350 - j*250
                reverse_row = True
                
                if j < 5:
                    VCSEL, VCSEL_parameters = create_one_VCSEL(full_mask, layer_data,
                                                                VCSEL_x, VCSEL_y,
                                                                p_ring_inner_1[i], p_ring_outer_1[i],
                                                                i, j,
                                                                reverse_row,
                                                                n_contact_outer, circle_tolerance)
                else:
                    VCSEL, VCSEL_parameters = create_one_VCSEL(full_mask, layer_data,
                                                                VCSEL_x, VCSEL_y,
                                                                p_ring_inner_2[i], p_ring_outer_2[i],
                                                                i, j,
                                                                reverse_row,
                                                                n_contact_outer, circle_tolerance)
                        
                
                # mask.add(*VCSEL.values())
                
                mesa_diameter        = VCSEL_parameters['mesa_diameter']
                mesa_radius          = mesa_diameter/2
                mesa_diameter_string = str(math.floor(mesa_diameter))
                
                if j == 0:
                    right_offset = 250
                    witness_mesa_right_x = VCSEL_x + right_offset
                    witness_mesa_right = create_circle(witness_mesa_right_x, VCSEL_y, mesa_radius, layer_data['mesa'], circle_tolerance)
                    # mask.add(witness_mesa_right)
                    full_mask['mesa'].add(witness_mesa_right)
                    
                    right_text_x = VCSEL_x + right_offset - 21
                    right_text_y = VCSEL_y + 10
                    top_mesa_label = create_mesa_label(right_text_x, VCSEL_y, mesa_diameter_string, layer_data['mesa'])
                    # mask.add(*top_mesa_label)
                    full_mask['mesa'].add(*top_mesa_label)
                    
                    open_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                          open_mesa_width, open_mesa_height, 
                                          layer_data['open_sidewalls'])
                    # mask.add(open_witeness_mesa)
                    full_mask['open_sidewalls'].add(open_witeness_mesa)
                    
                    witeness_mesa_etch = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                      mesa_etch_width, mesa_etch_height, 
                                                      layer_data['witness_mesa'])
                    # mask.add(witeness_mesa_etch)
                    full_mask['witness_mesa'].add(witeness_mesa_etch)
                    
                    open_etch_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                          open_mesa_width, open_mesa_height, 
                                                          layer_data['open_contacts'])
                    # mask.add(open_etch_witeness_mesa)
                    full_mask['open_contacts'].add(open_etch_witeness_mesa)
            
        
        
        
        p_ring_outer = np.array([9.5, 9.75, 10.0, 10.25, 10.0, 10.25, 10.5, 10.75, 11.0])
        p_ring_inner = p_ring_outer - 4.5
        
        mesa_size_major = 2*(p_ring_outer + 2)

        eccentricity = np.zeros(shape=(len(p_ring_outer), number_of_colums))
        
        eccentricity[0, :] = np.linspace(1, 0.895, 10)
        eccentricity[1, :] = np.linspace(1, 0.875, 10)
        eccentricity[2, :] = np.linspace(1, 0.85, 10)
        eccentricity[3, :] = np.linspace(1, 0.83, 10)
        eccentricity[4, :] = np.linspace(1, 0.81, 10)
        eccentricity[5, :] = np.linspace(1, 0.792, 10)
        eccentricity[6, :] = np.linspace(1, 0.773, 10)
        eccentricity[7, :] = np.linspace(1, 0.756, 10)
        eccentricity[8, :] = np.linspace(1, 0.74, 10)
        
        eccentricity_2 = np.linspace(1, 0.85, 10)
                
        mesa_size_minor = np.zeros(shape=(len(p_ring_outer), len(eccentricity[0, :])))
        
        for i in range(len(p_ring_outer)):
            for j in range(len(eccentricity[0,:])):
                mesa_size_minor[i, j] = 2*(p_ring_outer[i]*eccentricity[i,j] + 2)
        
        for i in range(number_of_rows):
        
            VCSEL_y = -300 - i*diff_row
            
            open_mesa_width  = 60
            open_mesa_height = 100
            
            reverse_row = False
            major_axis_001 = True
            for j in range(number_of_colums):
                VCSEL_x = -frame_size_x/2 + 350 + j*250
                
                
                VCSEL, VCSEL_parameters = create_one_ellip_VCSEL(full_mask, layer_data,
                                                                      VCSEL_x,  VCSEL_y,
                                                                      p_ring_inner[i], p_ring_outer[i],
                                                                      eccentricity[i,j], eccentricity_2[j], major_axis_001,
                                                                      i, j, reverse_row,
                                                                      n_contact_outer, circle_tolerance)
                    
                # else:
                #     VCSEL, VCSEL_parameters = create_one_ellip_VCSEL(full_mask, layer_data,
                #                                                   VCSEL_x,  VCSEL_y,
                #                                                   p_ring_inner[i], p_ring_outer[i],
                #                                                   eccentricity_large[j], eccentricity_2_large[j], major_axis_001,
                #                                                   i, j, reverse_row,
                #                                                   n_contact_outer, circle_tolerance)
                        
                        
                # mask.add(*VCSEL.values())
                
                mesa_diameter = VCSEL_parameters['mesa_diameter']
                mesa_radius   = mesa_diameter/2
                mesa_diameter_string = str(round(mesa_diameter))
                
                if j == 0:
                    
                    left_offset = -250
                    witness_mesa_left_x = VCSEL_x + left_offset
                    witness_mesa_left = create_circle(witness_mesa_left_x, VCSEL_y, (mesa_radius, mesa_size_minor[i, 4]/2), layer_data['mesa'], circle_tolerance)
                    # mask.add(witness_mesa_left)
                    full_mask['mesa'].add(witness_mesa_left)
                    
                    
                    left_text_x = VCSEL_x + left_offset - 21
                    left_text_y = VCSEL_y + 10
                    top_mesa_label = create_mesa_label(left_text_x, left_text_y, mesa_diameter_string, layer_data['mesa'])
                    # mask.add(*top_mesa_label)
                    full_mask['mesa'].add(*top_mesa_label)
                    
                    open_witeness_mesa = create_rectangle(witness_mesa_left_x, VCSEL_y,
                                                          open_mesa_width, open_mesa_height, 
                                                          layer_data['open_sidewalls'])
                    # mask.add(open_witeness_mesa)
                    full_mask['open_sidewalls'].add(open_witeness_mesa)
                    
                    witeness_mesa_etch = create_rectangle(witness_mesa_left_x, VCSEL_y,
                                                          mesa_etch_width, mesa_etch_height, 
                                                          layer_data['witness_mesa'])
                    # mask.add(witeness_mesa_etch)
                    full_mask['witness_mesa'].add(witeness_mesa_etch)
                    
                    open_etch_witeness_mesa = create_rectangle(witness_mesa_left_x, VCSEL_y,
                                                          open_mesa_width, open_mesa_height, 
                                                          layer_data['open_contacts'])
                    # mask.add(open_etch_witeness_mesa)
                    full_mask['open_contacts'].add(open_etch_witeness_mesa)
                    
                    
                    
                
                if j == 9:
                    
                    right_offset = 400
                    witness_mesa_right_x = VCSEL_x + right_offset
                    witness_mesa_right = create_circle(witness_mesa_right_x, VCSEL_y, (mesa_radius, mesa_size_minor[i, 9]/2), layer_data['mesa'], circle_tolerance)
                    # mask.add(witness_mesa_right)
                    full_mask['mesa'].add(witness_mesa_right)
                    
                    right_text_x = VCSEL_x + right_offset - 21
                    right_text_y = VCSEL_y + 10
                    top_mesa_label = create_mesa_label(right_text_x, right_text_y, mesa_diameter_string, layer_data['mesa'])
                    # mask.add(*top_mesa_label)
                    full_mask['mesa'].add(*top_mesa_label)
                    
                    open_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                          open_mesa_width, open_mesa_height, 
                                          layer_data['open_sidewalls'])
                    # mask.add(open_witeness_mesa)
                    full_mask['open_sidewalls'].add(open_witeness_mesa)
                    
                    witeness_mesa_etch = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                          mesa_etch_width, mesa_etch_height, 
                                                          layer_data['witness_mesa'])
                    # mask.add(witeness_mesa_etch)
                    full_mask['witness_mesa'].add(witeness_mesa_etch)
                    
                    open_etch_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                          open_mesa_width, open_mesa_height, 
                                                          layer_data['open_contacts'])
                    # mask.add(open_etch_witeness_mesa)
                    full_mask['open_contacts'].add(open_etch_witeness_mesa)
                
                
            reverse_row = True
            major_axis_001 = False
            for j in range(number_of_colums):
                VCSEL_x = +frame_size_x/2 - 350 - j*250
                
                
                VCSEL, VCSEL_parameters = create_one_ellip_VCSEL(full_mask, layer_data,
                                                                      VCSEL_x,  VCSEL_y,
                                                                      p_ring_inner[i], p_ring_outer[i],
                                                                      eccentricity[i, j], eccentricity_2[j], major_axis_001,
                                                                      i, j, reverse_row,
                                                                      n_contact_outer, circle_tolerance)
                # else:
                #     VCSEL, VCSEL_parameters = create_one_ellip_VCSEL(full_mask, layer_data,
                #                                                       VCSEL_x,  VCSEL_y,
                #                                                       p_ring_inner[i], p_ring_outer[i],
                #                                                       eccentricity_large[j], eccentricity_2_large[j], major_axis_001,
                #                                                       i, j, reverse_row,
                #                                                       n_contact_outer, circle_tolerance)
                # mask.add(*VCSEL.values())
                
                mesa_diameter = VCSEL_parameters['mesa_diameter']
                mesa_radius   = mesa_diameter/2
                mesa_diameter_string = str(round(mesa_diameter))
                
                if j == 0:
                    
                    right_offset = 250
                    witness_mesa_right_x = VCSEL_x + right_offset
                    witness_mesa_right = create_circle(witness_mesa_right_x, VCSEL_y, (mesa_size_minor[i, 4]/2, mesa_radius), layer_data['mesa'], circle_tolerance)
                    # mask.add(witness_mesa_right)
                    full_mask['mesa'].add(witness_mesa_right)
                    
                    right_text_x = VCSEL_x + right_offset - 21
                    right_text_y = VCSEL_y + 10
                    top_mesa_label = create_mesa_label(right_text_x, right_text_y, mesa_diameter_string, layer_data['mesa'])
                    # mask.add(*top_mesa_label)
                    full_mask['mesa'].add(*top_mesa_label)
                    
                    open_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                          open_mesa_width, open_mesa_height, 
                                          layer_data['open_sidewalls'])
                    # mask.add(open_witeness_mesa)
                    full_mask['open_sidewalls'].add(open_witeness_mesa)
                    
                    witeness_mesa_etch = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                      mesa_etch_width, mesa_etch_height, 
                                                      layer_data['witness_mesa'])
                    # mask.add(witeness_mesa_etch)
                    full_mask['witness_mesa'].add(witeness_mesa_etch)
                    
                    
                    open_etch_witeness_mesa = create_rectangle(witness_mesa_right_x, VCSEL_y,
                                                          open_mesa_width, open_mesa_height, 
                                                          layer_data['open_contacts'])
                    # mask.add(open_etch_witeness_mesa)
                    full_mask['open_contacts'].add(open_etch_witeness_mesa)

    
    ###### ADD ALL LABELS ###################
    label_x = 230
    y_margin_labels = 1920
    label_y = -chip_size_y/2 + y_margin_labels
    
    label_distance_y = 60
    
    p_ring_label = create_mask_label(label_x, label_y, '1. TC + ALIGN     (CF)', layer_data['p_ring'])
    
    add_list_to_layer(p_ring_label, full_mask, layer_data_reversed)
    # mask.add(*p_ring_label)
    
    top_mesa_label = create_mask_label(label_x, label_y-label_distance_y, '2. TOP MESA       (CF)', layer_data['mesa'])
    
    add_list_to_layer(top_mesa_label, full_mask, layer_data_reversed)
    # mask.add(*top_mesa_label)
    
    open_side_wall_label = create_mask_label(label_x, label_y - 2*label_distance_y, '3. SiNx OPEN      (DF)', layer_data['open_sidewalls'])
    
    add_list_to_layer(open_side_wall_label, full_mask, layer_data_reversed)
    # mask.add(*open_side_wall_label)
    
    witness_mesa_label = create_mask_label(label_x, label_y - 3*label_distance_y, '4. WITNESS OPEN   (DF)', layer_data['witness_mesa'])
    
    add_list_to_layer(witness_mesa_label, full_mask, layer_data_reversed)
    #mask.add(*witness_mesa_label)
    
    n_ring_label = create_mask_label(label_x, label_y - 4*label_distance_y, '5. BOTTOM CONTACT (DF)', layer_data['n_ring'])
    
    add_list_to_layer(n_ring_label, full_mask, layer_data_reversed)
    #mask.add(*n_ring_label)
    
    open_contacts_label = create_mask_label(label_x, label_y - 5*label_distance_y, '6. CONTACT ETCH   (CF)', layer_data['open_contacts'])
    
    add_list_to_layer(open_contacts_label, full_mask, layer_data_reversed)
    # mask.add(*open_contacts_label)
    
    contact_pads_label = create_mask_label(label_x, label_y - 6*label_distance_y, '7. CONTACT PADS   (DF)', layer_data['contact_pads'])
    
    add_list_to_layer(contact_pads_label, full_mask, layer_data_reversed)
    # mask.add(*contact_pads_label)
    
    bond_pads_label = create_mask_label(label_x, label_y - 7*label_distance_y, '8. BOND PADS      (DF)', layer_data['bond_pads'])
    
    add_list_to_layer(bond_pads_label, full_mask, layer_data_reversed)
    # mask.add(*bond_pads_label)
    
    MS_align_label = create_mask_label(label_x, label_y - 8*label_distance_y, '9. MS ALIGN       (CF)', layer_data['MS_align'])
    
    add_list_to_layer(MS_align_label, full_mask, layer_data_reversed)
    # mask.add(*MS_align_label)
    
    # MESA DIAMETER = 2*(top_ring + 2)
    mesa_size = 2*(9+2)
    
    ### Add cell to main layer
    for layer in full_mask.keys():
        cell_layer = gdstk.Reference(full_mask[layer])
        mask.add(cell_layer)
        
    # def add_cell(mask, cell, x_offset, y_offset):
    #     for i in cell:
    #         i.translate((x_offset, y_offset))
    #         i.layer = 1
    #         mask.add(i)
            
    # MS_align_cell = full_mask['MS_align'].copy('MS_align_row')

    # add_cell(mask, MS_align_cell.polygons, 0, 0)

    # Save the library in a file called 'first.gds'.
    if save_layout:
        lib.write_gds(mask_folder + mask_name + '.gds')
        # lib.write_gds(outfile)

    

if  __name__ == '__main__':
    main()
