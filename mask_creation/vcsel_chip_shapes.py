#%%

import gdstk
from generic_shapes import create_rectangle

def create_a_mark_vernier_calipers(x, y,
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
            
def create_a_mark(x, y,
                          thickness, length,
                          layer_data):
        
        return create_a_mark_vernier_calipers(x, y,
                                     thickness, length,
                                     0, 0,
                                     0, 0,
                                     0, 0, 0,
                                     False,
                                     layer_data)