#%%

import gdstk
from generic_shapes import create_rectangle
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
    
    
    


        
        
        
    