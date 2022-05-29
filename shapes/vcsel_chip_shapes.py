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
                          layer_data):
    
    alignment_polygons = []
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
    
    alignment_polygons.append(alignment_cross.rotate(rotation))
    
    if with_calipers:
        for i in range(marks_y_direction):
            alignment_polygons.append(create_rectangle(key, x - x_offset_rectangles, y + first_y_offset + i*repeating_y_offset, 
                                                       rectangle_width, rectangle_height, 
                                                       layer_data, rotation=rotation))
            
            alignment_polygons.append(create_rectangle(key, x - x_offset_rectangles, y - first_y_offset - i*repeating_y_offset, 
                                                       rectangle_width, rectangle_height, 
                                                       layer_data, rotation=rotation))
            
        for i in range(marks_y_direction):
            alignment_polygons.append(create_rectangle(key, x + first_y_offset + i*repeating_y_offset, y + y_offset_rectangles, 
                                                       rectangle_height, rectangle_width, 
                                                       layer_data, rotation=rotation))
            
            alignment_polygons.append(create_rectangle(key, x - first_y_offset - i*repeating_y_offset, y + y_offset_rectangles, 
                                                       rectangle_height, rectangle_width, 
                                                       layer_data, rotation=rotation))
            
            
    return alignment_polygons

def create_a_mark(key, 
                  x, y,
                  thickness, length,
                  with_calipers, rotation,
                  layer_data, left_side=True):
    
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
    
    return create_generic_a_mark(key, 
                                 x, y,
                                 thickness, length,
                                 x_offset_rectangles, y_offset_rectangles,
                                 rectangle_width, rectangle_height,
                                 first_y_offset, repeating_y_offset, marks_y_direction,
                                 with_calipers, rotation,
                                 layer_data)         

def create_initial_a_mark(key, 
                          x, y,
                          with_calipers, rotation,
                          layer_data, left_side=True):
    
    
    
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
    
    return create_generic_a_mark(key, 
                                 x, y,
                                 thickness, length,
                                 x_offset_rectangles, y_offset_rectangles,
                                 rectangle_width, rectangle_height,
                                 first_y_offset, repeating_y_offset, marks_y_direction,
                                 with_calipers, rotation,
                                 layer_data)

def create_DD_a_mark(key, 
                      x, y,
                      with_calipers, rotation,
                      layer_data, left_side=True):
    
    a_mark_polygon = []
    
    length = 200
    thickness = 24
    
    rectangle_width = 30
    rectangle_height = 15
    
    if left_side:
        x_offset_rectangles = 175
    else:
        x_offset_rectangles = -175
        
    y_offset_rectangles = 175
    
    first_y_offset = 26
    repeating_y_offset = 30.5
    marks_y_direction = 5   
    
    a_mark = create_generic_a_mark(key, 
                                   x, y,
                                   thickness, length,
                                   x_offset_rectangles, y_offset_rectangles,
                                   rectangle_width, rectangle_height,
                                   first_y_offset, repeating_y_offset, marks_y_direction,
                                   with_calipers, rotation,
                                   layer_data)

    thickness_cutout = 12
    
    a_mark_cut = create_a_mark(key, 
                               x, y,
                               thickness_cutout, length,
                               False, rotation,
                               layer_data, left_side=True)

    
    a_mark = gdstk.boolean(a_mark, a_mark_cut, 'not',
                            layer=layer_data[key]['layer_number'], datatype=layer_data[key]['datatype'])
    
    for polygon in a_mark:
        a_mark_polygon.append(polygon)
        
    return a_mark_polygon

def create_DC_a_mark(key, 
                     x, y,
                     with_calipers, rotation,
                     aligment_mark_offset,
                     layer_data, left_side=True):
    
    a_mark_polygon = []
    
    a_mark = create_DD_a_mark(key, 
                              x, y,
                              with_calipers, rotation,
                              layer_data)
    
    covered_a_mark = create_rectangle(key, x, y, aligment_mark_offset, aligment_mark_offset, layer_data).rotate(rotation)
    
    for cutout in a_mark:
        covered_a_mark = gdstk.boolean(covered_a_mark, cutout, 'not',
                            layer=layer_data[key]['layer_number'], datatype=layer_data[key]['datatype'])

    return covered_a_mark
    
    
       
def create_initial_a_marks_all_corners(key, frame_size_x, frame_size_y, colums_of_alignment_marks, layer_data):
    
    alignment_polygons = []
    
    aligment_mark_offset = 500
    pos = layer_data[key]['a_mark_position']
    
    pos_x = (pos - 2)%colums_of_alignment_marks
    
    if pos < (colums_of_alignment_marks + 2):
        pos_y = 0
    else:
        pos_y = 1
        
    with_calipers = layer_data[key]['calipers']    
    
    for layer_key in layer_data.keys():
        if layer_data[layer_key]['layer_number'] == 1:
            key = layer_key
    
    x = -frame_size_x/2 + aligment_mark_offset/2 + pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    
    alignment_polygons.append(create_initial_a_mark(key, 
                                                    x, y,
                                                    with_calipers, rotation,
                                                    layer_data))
    
    rotation = np.pi
    alignment_polygons.append(create_initial_a_mark(key, 
                                            x, y,
                                            with_calipers, rotation,
                                            layer_data))
    
    x =  frame_size_x/2 - aligment_mark_offset/2 - pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    left_side = False
    
    alignment_polygons.append(create_initial_a_mark(key, 
                                            x, y,
                                            with_calipers, rotation,
                                            layer_data, left_side=left_side))
    
    

    rotation = np.pi
    alignment_polygons.append(create_initial_a_mark(key, 
                                                    x, y,
                                                    with_calipers, rotation,
                                                    layer_data, left_side=left_side))
    
    return alignment_polygons
   
def create_a_marks_DD_all_corners(key, 
                                  frame_size_x, frame_size_y, 
                                  colums_of_alignment_marks, 
                                  aligment_mark_offset, layer_data):
    
    alignment_polygons = []
    
    pos = layer_data[key]['a_mark_position']
    
    pos_x = (pos - 2)%colums_of_alignment_marks
    
    if pos < (colums_of_alignment_marks + 2):
        pos_y = 0
    else:
        pos_y = 1
        
    with_calipers = layer_data[key]['calipers']    
    
    x = -frame_size_x/2 + aligment_mark_offset/2 + pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    
    alignment_polygons.append(create_DD_a_mark(key, 
                                            x, y,
                                            with_calipers, rotation,
                                            layer_data))
    
    rotation = np.pi
    alignment_polygons.append(create_DD_a_mark(key, 
                                            x, y,
                                            with_calipers, rotation,
                                            layer_data))
    
    x =  frame_size_x/2 - aligment_mark_offset/2 - pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    left_side = False
    
    alignment_polygons.append(create_DD_a_mark(key, 
                                            x, y,
                                            with_calipers, rotation,
                                            layer_data, left_side=left_side))

    rotation = np.pi
    alignment_polygons.append(create_DD_a_mark(key, 
                                                    x, y,
                                                    with_calipers, rotation,
                                                    layer_data, left_side=left_side))
    
    return alignment_polygons

def create_a_marks_DC_all_corners(key, frame_size_x, frame_size_y, colums_of_alignment_marks, aligment_mark_offset, layer_data):
    
    alignment_polygons = []
    pos = layer_data[key]['a_mark_position']
    
    pos_x = (pos - 2)%colums_of_alignment_marks
    
    if pos < (colums_of_alignment_marks + 2):
        pos_y = 0
    else:
        pos_y = 1
        
    with_calipers = layer_data[key]['calipers']    
    
    x = -frame_size_x/2 + aligment_mark_offset/2 + pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    
    alignment_polygons.append(create_DC_a_mark(key, 
                                               x, y,
                                               with_calipers, rotation,
                                               aligment_mark_offset,
                                               layer_data))
    
    rotation = np.pi
    alignment_polygons.append(create_DC_a_mark(key, 
                                               x, y,
                                               with_calipers, rotation,
                                               aligment_mark_offset,
                                               layer_data))
    
    x =  frame_size_x/2 - aligment_mark_offset/2 - pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    
    rotation = 0
    left_side = False
    
    alignment_polygons.append(create_DC_a_mark(key, 
                                            x, y,
                                            with_calipers, rotation,
                                            aligment_mark_offset,
                                            layer_data, left_side=left_side))

    rotation = np.pi
    alignment_polygons.append(create_DC_a_mark(key, 
                                                    x, y,
                                                    with_calipers, rotation,
                                                    aligment_mark_offset,
                                                    layer_data, left_side=left_side))
    
    return alignment_polygons

def cover_chip_DD(key, frame_size_x, frame_size_y, colums_of_alignment_marks, aligment_mark_offset, layer_data):
    cover_polygons = []
    
    pos = layer_data[key]['a_mark_position']
    
    pos_x = (pos - 2)%colums_of_alignment_marks
    
    if pos < (colums_of_alignment_marks + 2):
        pos_y = 0
    else:
        pos_y = 1
    
    cover_upper_marks = gdstk.Polygon([(-frame_size_x/2,  frame_size_y/2),
                                       (frame_size_x/2,   frame_size_y/2),
                                       (frame_size_x/2,   frame_size_y/2 - 2*aligment_mark_offset),
                                       (-frame_size_x/2,  frame_size_y/2 - 2*aligment_mark_offset)],
                                       layer=layer_data[key]['layer_number'],
                                       datatype=layer_data[key]['datatype'])
    
    
    x = -frame_size_x/2 + aligment_mark_offset/2 + pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    cutout = create_rectangle(key, x, y, aligment_mark_offset, aligment_mark_offset, layer_data)
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, cutout, 'not', layer=layer_data[key]['layer_number'],
                                                                        datatype=layer_data[key]['datatype'])
    
    x =  frame_size_x/2 - aligment_mark_offset/2 - pos_x*aligment_mark_offset
    y =  frame_size_y/2 - aligment_mark_offset/2 - pos_y*aligment_mark_offset
    cutout = create_rectangle(key, x, y, aligment_mark_offset, aligment_mark_offset, layer_data)
    
    cover_upper_marks = gdstk.boolean(cover_upper_marks, cutout, 'not', layer=layer_data[key]['layer_number'],
                                                                        datatype=layer_data[key]['datatype'])
    cover_lower_polygons = []
    
    for i in cover_upper_marks:
       cover_polygons.append(i)
       cover_lower_polygons.append(i.copy())
       
    lower_cutout = create_rectangle(key, 0, 0, frame_size_x - aligment_mark_offset*8, frame_size_y, layer_data)
    cover_lower_polygons = gdstk.boolean(cover_lower_polygons, lower_cutout, 'not', layer=layer_data[key]['layer_number'],
                                                                                    datatype=layer_data[key]['datatype'])
    
        
    for i in cover_lower_polygons:
        i.rotate(np.pi)
        cover_polygons.append(i)
    
      
    return cover_polygons

def cover_chip_DC(key, chip_size_x, chip_size_y, frame_size_x, frame_size_y, layer_data):
    
    entire_chip = create_rectangle(key, 0, 0, chip_size_x, chip_size_y, layer_data)
    
    frame = create_rectangle(key, 0, 0, frame_size_x, frame_size_y, layer_data)
    
    out_side_cover = gdstk.boolean(entire_chip, frame, 'not', layer=layer_data[key]['layer_number'],
                                    datatype=layer_data[key]['datatype'])
    
    return out_side_cover
    
    

def create_a_marks_all_layers(chip_size_x, chip_size_y,
                              frame_size_x, frame_size_y,
                              colums_of_alignment_marks, aligment_mark_offset,
                              layer_data):
    
    alignment_polygons = ([], [], [], [])

    for key in layer_data.keys():
        pos = layer_data[key]['a_mark_position']
        
        if layer_data[key]['layer_number'] != 1:
            if isinstance(pos, int):    
                if layer_data[key]['data_parity'] == 'DD':
                    
                    alignment_polygons[0].append(create_a_marks_DD_all_corners(key, 
                                                                               frame_size_x, frame_size_y, 
                                                                               colums_of_alignment_marks, 
                                                                               aligment_mark_offset,
                                                                               layer_data))
                    
                    alignment_polygons[1].append(cover_chip_DD(key, 
                                                               frame_size_x, frame_size_y, 
                                                               colums_of_alignment_marks, 
                                                               aligment_mark_offset,
                                                               layer_data))
                    
                    
                if layer_data[key]['data_parity'] == 'DC':
                    alignment_polygons[2].append(create_a_marks_DC_all_corners(key, 
                                                                               frame_size_x, frame_size_y, 
                                                                               colums_of_alignment_marks, 
                                                                               aligment_mark_offset,
                                                                               layer_data))
                    alignment_polygons[3].append(cover_chip_DC(key, chip_size_x, chip_size_y,
                                                                frame_size_x, frame_size_y,
                                                                layer_data))
                    
                    
                    
                
    return alignment_polygons
    
def create_initial_a_marks_all_layers(frame_size_x, frame_size_y, colums_of_alignment_marks, layer_data):
    alignment_polygons = []

    for key in layer_data.keys():
        pos = layer_data[key]['a_mark_position']
        
        if isinstance(pos, int):
                alignment_polygons.append(create_initial_a_marks_all_corners(key, 
                                                                 frame_size_x, frame_size_y, 
                                                                 colums_of_alignment_marks, 
                                                                 layer_data))
    
    return alignment_polygons
            
def create_orientation_arrow(key, x, y,
                             arrow_head, arrow_base,
                             layer_data):
    
    return gdstk.Polygon([(x - arrow_head/2, y),
                          (x - arrow_head, y),
                          (x,                y + arrow_head),
                          (x + arrow_head,   y),
                          (x + arrow_head/2, y),
                          (x + arrow_head/2, y - arrow_base),
                          (x - arrow_head/2, y - arrow_base)],
                           layer=layer_data[key]['layer_number'],
                           datatype=layer_data[key]['datatype'])
    
def create_TLM_circles(ring_layer, x, y, layer_data, circle_tolerance):
    TLM_circle_layers = []
    
    TLM_circles_x_size = 1100
    TLM_circles_y_size = 200
    TLM_circles = create_rectangle(ring_layer, x, y, TLM_circles_x_size, TLM_circles_y_size, layer_data)
    
    x_offset = -400
    middle_circle_x = x + x_offset
    x_offset = np.array([0, 200, 200, 200, 200])
    
    
    inner_annulus = 50
    outer_annulus = np.array([75, 70, 65, 60, 55])

    
    for i, x_offset in enumerate(x_offset):
        middle_circle_x = middle_circle_x + x_offset
    
        middle_annulus = create_annulus(ring_layer, middle_circle_x, y, 
                                        inner_annulus, outer_annulus[i], 
                                        layer_data, circle_tolerance)
        
        TLM_circles = gdstk.boolean(TLM_circles, middle_annulus, 'not', 
                                    layer=layer_data[ring_layer]['layer_number'],
                                    datatype=layer_data[ring_layer]['datatype'])
    
    for polygons in TLM_circles:
        TLM_circle_layers.append(polygons)
    
    
    cover_margin_x = 10
    cover_margin_y = 10
    
    cover_size_x = TLM_circles_x_size + cover_margin_x
    cover_size_y = TLM_circles_y_size + cover_margin_y
    create_rectangle('mesa', x, y, cover_size_x, cover_size_y, layer_data)
    
    create_rectangle('open_contacts', x, y, cover_size_x, cover_size_y, layer_data)
    
    contact_margin = 10
    TLM_contact_x_size = TLM_circles_x_size - contact_margin
    TLM_contact_y_size = TLM_circles_y_size - contact_margin
    
    TLM_contact = create_rectangle('contact_pads', x, y, TLM_contact_x_size, TLM_contact_y_size, layer_data)
    
    contact_annulus_margin = 5
    contact_inner_annulus = inner_annulus - contact_annulus_margin
    contact_outer_annulus = outer_annulus + contact_annulus_margin
    
    ## NEED TO RESET VARIABLE THIS IS STUPID
    x_offset = -400
    middle_circle_x = x + x_offset
    x_offset = np.array([0, 200, 200, 200, 200])
    
    for i, x_offset in enumerate(x_offset):
        middle_circle_x = middle_circle_x + x_offset
    
        middle_annulus = create_annulus('contact_pads', middle_circle_x, y, 
                                        contact_inner_annulus, contact_outer_annulus[i], 
                                        layer_data, circle_tolerance)
        
        TLM_contact = gdstk.boolean(TLM_contact, middle_annulus, 'not', 
                                    layer=layer_data['contact_pads']['layer_number'],
                                    datatype=layer_data['contact_pads']['datatype'])
    
    
    for polygons in TLM_circles:
        TLM_circle_layers.append(polygons)
        
        
    return TLM_circle_layers
        
def create_TLM_pads(pad_layer, x, y, layer_data):
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
        TLM_pads.append(create_rectangle(pad_layer, x_pads, y, pad_width, pad_height, layer_data))
        
    
    cover_margin_x = 10
    cover_margin_y = 10
    
    cover_size_x = -x_fifth_offset + pad_width + cover_margin_x
    cover_size_y = pad_height + cover_margin_y
    TLM_pads.append(create_rectangle('mesa', x + x_fifth_offset/2, y, cover_size_x, cover_size_y, layer_data))
    
    TLM_pads.append(create_rectangle('open_contacts', x + x_fifth_offset/2, y, cover_size_x, cover_size_y, layer_data))
    
    
    contact_margin = 10
    contact_width = pad_width - contact_margin
    contact_height = pad_height - contact_margin
    
    for x_pads in x_positions:
        TLM_pads.append(create_rectangle('contact_pads', x_pads, y, contact_width, contact_height, layer_data))
        
    return TLM_pads

def create_label(key, x, y, size, text, layer_data):
    label_polygons = []
    
    polygons = gdstk.text(text, size,
                          (x, y),
                          layer=layer_data[key]['layer_number'],
                          datatype=layer_data[key]['datatype'])
    
    for polygon in polygons:
        label_polygons.append(polygon)
        
    return label_polygons
        
def create_mask_label(key, x, y, text, layer_data):
    size = 60
    
    return create_label(key, x, y, size, text, layer_data)
        
def create_all_labels(x, y, label_distance_y, layer_data):
    label_polygons = []
    
    for i, key in enumerate(layer_data.keys()):
        text = layer_data[key]['label']
        if text != 'NO_LABEL':
            y_pos = y - i*label_distance_y
            label_polygons.append(create_mask_label(key, x, y_pos, text, layer_data))
    
    return label_polygons

