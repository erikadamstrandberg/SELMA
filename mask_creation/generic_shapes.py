#%%

import gdstk
import numpy as np


def create_annulus(x, y,
                   inner, outer,
                   layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                         outer, 
                         inner_radius=inner, 
                         initial_angle=0,
                         final_angle=2*np.pi,
                         layer=layer_data['layer_number'],
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
                         layer=layer_data['layer_number'],
                         datatype=layer_data['datatype'],
                         tolerance=tolerance
                         )

def create_circle(x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius, 
                        layer=layer_data['layer_number'],
                        datatype=layer_data['datatype'],
                        tolerance=tolerance
                        )

def create_rectangle(key, x, y, x_size, y_size, layer_data, full_mask):
    
    right_x = x + x_size/2
    left_x  = x - x_size/2
    
    upper_y = y + y_size/2
    lower_y = y - y_size/2
    
    full_mask[key] = gdstk.Polygon([(right_x, upper_y),
                               (right_x, lower_y),
                               (left_x,  lower_y),
                               (left_x,  upper_y)],
                              layer=layer_data[key]['layer_number'],
                              datatype=layer_data[key]['datatype'])
    
    