#%%

import gdstk
import numpy as np


def create_annulus(key, x, y,
                   inner, outer,
                   layer_data, 
                   tolerance):
    
    polygon = gdstk.ellipse(np.array([x, y]), 
                         outer, 
                         inner_radius=inner, 
                         initial_angle=0,
                         final_angle=2*np.pi,
                         layer=layer_data[key]['layer_number'],
                         datatype=layer_data[key]['datatype'],
                         tolerance=tolerance
                         )
    
    return polygon

def create_half_annulus(key, x, y,
                        inner, outer,
                        initial_angle, final_angle,
                        layer_data, 
                        tolerance):
    
    polygon = gdstk.ellipse(np.array([x, y]), 
                         outer, 
                         inner_radius=inner, 
                         initial_angle=initial_angle,
                         final_angle=final_angle,
                         layer=layer_data[key]['layer_number'],
                         datatype=layer_data[key]['datatype'],
                         tolerance=tolerance
                         )
    
    return polygon

def create_circle(key, x, y, radius, layer_data, tolerance):
    
    polygon = gdstk.ellipse(np.array([x, y]), 
                            radius, 
                            layer=layer_data[key]['layer_number'],
                            datatype=layer_data[key]['datatype'],
                            tolerance=tolerance)
    
    return polygon

def create_rectangle(key, x, y, x_size, y_size, layer_data, rotation=0):
    
    right_x = x + x_size/2
    left_x  = x - x_size/2
    
    upper_y = y + y_size/2
    lower_y = y - y_size/2
    
    polygon = gdstk.Polygon([(right_x, upper_y),
                             (right_x, lower_y),
                             (left_x,  lower_y),
                             (left_x,  upper_y)],
                            layer=layer_data[key]['layer_number'],
                            datatype=layer_data[key]['datatype']).rotate(rotation)
    
    
    return polygon

def create_polygon1(key, x1, y1, x2, y2, x3, y3, x4, y4, layer_data, rotation=0):
      
    polygon = gdstk.Polygon([(x1, y1),
                             (x2, y2),
                             (x3, y3),
                             (x4, y4)],
                            layer=layer_data[key]['layer_number'],
                            datatype=layer_data[key]['datatype']).rotate(rotation)
    
    return polygon


def create_rotated_rectangle(key, x, y, x_size, y_size, layer_data, rotation):
    x1= x_size/2
    y1= y_size/2
    the = rotation
    
    #Rotate the angles, use X = x*cos(θ) - y*sin(θ) and Y = x*sin(θ) + y*cos(θ)
    
    rotatedX1 = x1*np.cos(the) - y1*np.sin(the)
    rotatedY1 = x1*np.sin(the) + y1*np.cos(the)
    
    rotatedX2 = -x1*np.cos(the) - y1*np.sin(the)
    rotatedY2 = -x1*np.sin(the) + y1*np.cos(the)
    
    rotatedX3 = x1*np.cos(the) + y1*np.sin(the)
    rotatedY3 = x1*np.sin(the) - y1*np.cos(the)
    
    rotatedX4 = -x1*np.cos(the) + y1*np.sin(the)
    rotatedY4 = -x1*np.sin(the) - y1*np.cos(the)

    
    polygon = gdstk.Polygon([(x + rotatedX1, y + rotatedY1),
                             (x + rotatedX3, y + rotatedY3),
                             (x + rotatedX4, y + rotatedY4),
                             (x + rotatedX2, y + rotatedY2)],
                            layer=layer_data[key]['layer_number'],
                            datatype=layer_data[key]['datatype']).rotate(0)
    
    
    return polygon

