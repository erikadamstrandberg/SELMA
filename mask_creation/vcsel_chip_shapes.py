#%%

import gdstk
from generic_shapes import create_rectangle, create_annulus
import numpy as np

def create_generic_a_mark(key, 
                  x, y,
                  thickness, length,
                  x_offset_rectangles, y_offset_rectangles,
                  rectangle_width, rectangle_height,
                  first_y_offset, repeating_y_offset, marks_y_direction,
                  with_calipers, rotation,
                  layer_data, full_mask):
    
    
    alignment_cross = gdstk.Polygon([(x + thickness/2,      y + thickness/2),
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
                                     layer=layer_data[key]['layer_number'],
                                     datatype=layer_data[key]['datatype'])
    
    full_mask[key].append(alignment_cross.rotate(rotation))
    
    if with_calipers:
        for i in range(marks_y_direction):
            create_rectangle(key, x - x_offset_rectangles, y + first_y_offset + i*repeating_y_offset, 
                             rectangle_width, rectangle_height, 
                             layer_data, full_mask, rotation=rotation)
            
            create_rectangle(key, x - x_offset_rectangles, y - first_y_offset - i*repeating_y_offset, 
                             rectangle_width, rectangle_height, 
                             layer_data, full_mask, rotation=rotation)
            
        for i in range(marks_y_direction):
            create_rectangle(key, x + first_y_offset + i*repeating_y_offset, y + y_offset_rectangles, 
                             rectangle_height, rectangle_width, 
                             layer_data, full_mask, rotation=rotation)
            
            create_rectangle(key, x - first_y_offset - i*repeating_y_offset, y + y_offset_rectangles, 
                             rectangle_height, rectangle_width, 
                             layer_data, full_mask, rotation=rotation)
            

def create_a_mark(key, 
                  x, y,
                  with_calipers, rotation,
                  layer_data, full_mask, left_side=True):
    
    
    
    thickness = 8
    length    = 200
    
    rectangle_width = 30
    rectangle_height = 15
    
    if left_side:
        x_offset_rectangles = 190
    else:
        x_offset_rectangles = -190
        
    y_offset_rectangles = 190
    
    first_y_offset = 25
    repeating_y_offset = 30
    marks_y_direction = 5     
    
    create_generic_a_mark(key, 
                          x, y,
                          thickness, length,
                          x_offset_rectangles, y_offset_rectangles,
                          rectangle_width, rectangle_height,
                          first_y_offset, repeating_y_offset, marks_y_direction,
                          with_calipers, rotation,
                          layer_data, full_mask)
    

def create_a_marks_all_corners(key, frame_size_x, frame_size_y, colums_of_alignment_marks, layer_data, full_mask):
    
    aligment_mark_offset = 500
    pos = layer_data[key]['a_mark_position']
    
    pos_x = (pos - 1)%colums_of_alignment_marks
    
    if pos < (colums_of_alignment_marks + 1):
        pos_y = 0
    else:
        pos_y = 1
    
    x = -frame_size_x/2 + aligment_mark_offset/2 + pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    
    create_a_mark(key, 
                  x, y,
                  layer_data[key]['calipers'], rotation,
                  layer_data, full_mask)
    
    rotation = np.pi
    create_a_mark(key, 
                  x, y,
                  layer_data[key]['calipers'], rotation,
                  layer_data, full_mask)
    
    x =  frame_size_x/2 - aligment_mark_offset/2 - pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    left_side = False
    
    create_a_mark(key, 
                  x, y,
                  layer_data[key]['calipers'], rotation,
                  layer_data, full_mask, left_side=left_side)

    rotation = np.pi
    create_a_mark(key, 
                  x, y,
                  layer_data[key]['calipers'], rotation,
                  layer_data, full_mask, left_side=left_side)
    
    
def create_a_marks_all_layers(frame_size_x, frame_size_y, colums_of_alignment_marks, layer_data, full_mask):
    
    for key in layer_data.keys():
        pos = layer_data[key]['a_mark_position']
        
        if isinstance(pos, int):
            create_a_marks_all_corners(key, 
                                       frame_size_x, frame_size_y, 
                                       colums_of_alignment_marks, 
                                       layer_data, full_mask)
    
def create_orientation_arrow(key, x, y,
                             arrow_head, arrow_base,
                             layer_data, full_mask):
    
    
    print(layer_data[key])
    full_mask[key].append(gdstk.Polygon([(x - arrow_head/2, y),
                          (x - arrow_head, y),
                          (x,                y + arrow_head),
                          (x + arrow_head,   y),
                          (x + arrow_head/2, y),
                          (x + arrow_head/2, y - arrow_base),
                          (x - arrow_head/2, y - arrow_base)],
                           layer=layer_data[key]['layer_number'],
                           datatype=layer_data[key]['datatype']))
    
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
    
    
    


        
        
        
    