#%%

import os 

import numpy as np
import matplotlib.pyplot as plt

from scipy import constants
c     = constants.speed_of_light
mu_0  = constants.mu_0
eps_0 = constants.epsilon_0

import gdstk 

from pathlib import Path
SELMA_path = Path(__file__).parent.resolve()

def create_rectangle(key, x, y, x_size, y_size, layer_data):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer_data[key]['layer'],
                         datatype=layer_data[key]['datatype'])

def create_circle(key, x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius, 
                        layer=layer_data[key]['layer'],
                        datatype=layer_data[key]['datatype'],
                        tolerance=tolerance
                        )

def create_mask_label(x, y, text, layer_data):
    height = 80
    
    return gdstk.text(text, height,
                       (x, y),
                       layer=layer_data['layer'],
                       datatype=layer_data['datatype'])

def create_annulus(key, x, y,
                   inner, outer,
                   layer_data, 
                   tolerance):
    
    polygon = gdstk.ellipse(np.array([x, y]), 
                         outer, 
                         inner_radius=inner, 
                         initial_angle=0,
                         final_angle=2*np.pi,
                         layer=layer_data[key]['layer'],
                         datatype=layer_data[key]['datatype'],
                         tolerance=tolerance
                         )
    
    return polygon

def add_grating(grating_x, grating_y, grating_radius, grating_period, grating_duty_cycle, theta, full_mask, layer_data, circle_tolerance):
    grating_diameter = 2*grating_radius
    grating_width = grating_period*grating_duty_cycle
    
    grating_polygons = []
    number_of_lines_one_way = int(grating_diameter//grating_period)//2 + 1
    
    for i in range(number_of_lines_one_way):
        grating_line_width = np.sqrt(grating_diameter**2 - 4*(i*grating_period + grating_width/2)**2)
        grating_line = create_rectangle('pol_grating', grating_x, grating_y + i*grating_period, grating_line_width, grating_width, layer_data)
        grating_polygons.append(grating_line)
        
    for i in range(1, number_of_lines_one_way):
        grating_line_width = np.sqrt(grating_diameter**2 - 4*(i*grating_period + grating_width/2)**2)
        grating_line = create_rectangle('pol_grating', grating_x, grating_y - i*grating_period, grating_line_width, grating_width, layer_data)
        grating_polygons.append(grating_line)
        
    for polygon in grating_polygons:
        full_mask['pol_grating'].add(polygon.rotate(theta, center=(grating_x, grating_y)))
        
def add_grating_and_mode_filter(grating_x, grating_y, grating_radius, grating_period, grating_duty_cycle, theta, full_mask, layer_data, circle_tolerance):
    grating_diameter = 2*grating_radius
    grating_width = grating_period*grating_duty_cycle
    
    # grating_polygons = []
    number_of_lines_one_way = int(grating_diameter//grating_period)//2 + 1
    
    grating_and_mode_filter = create_annulus('pol_grating', grating_x, grating_y, grating_radius/2, grating_radius, layer_data, circle_tolerance)
    
    for i in range(number_of_lines_one_way):
        grating_line_width = np.sqrt(grating_diameter**2 - 4*(i*grating_period + grating_width/2)**2)
        grating_line = create_rectangle('pol_grating', grating_x, grating_y + i*grating_period, grating_line_width, grating_width, layer_data)
        
        grating_and_mode_filter = gdstk.boolean(grating_and_mode_filter, grating_line, 'or', layer=layer_data['pol_grating']['layer'],datatype=layer_data['pol_grating']['datatype'])
        

    for i in range(1, number_of_lines_one_way):
        grating_line_width = np.sqrt(grating_diameter**2 - 4*(i*grating_period + grating_width/2)**2)
        grating_line = create_rectangle('pol_grating', grating_x, grating_y - i*grating_period, grating_line_width, grating_width, layer_data)
        grating_and_mode_filter = gdstk.boolean(grating_and_mode_filter, grating_line, 'or', layer=layer_data['pol_grating']['layer'],datatype=layer_data['pol_grating']['datatype'])
        
        
    for polygon in grating_and_mode_filter:
        full_mask['pol_grating'].add(polygon.rotate(theta, center=(grating_x, grating_y)))
        

def main():
    ## SETUP VARIABLES ##
    
    mask_name   = 'POL_MODE_CALIBRATION_v1'
    
    # Name of cell
    cell_name   = 'POL_MODE_CALIBRATION_v1'
    
    save_layout = True
    
    # Set units and precision for layout
    unit      = 1.0e-6
    precision = 1.0e-10
    circle_tolerance = 0.00001
    
    ## CREATE THE MASK ##
    # The GDSII file is called a library, which contains multiple cells.
    lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
    gdstk.Library()
    
    ## MAIN CELL
    mask = lib.new_cell(cell_name)
    
    ## LAYER DATA
    pixalated_circles_layer = 1
    lables_layer = 2
    chip_layer = 3
    
    layer_data = {
        'pol_grating': {'layer': pixalated_circles_layer, 'datatype': 1},
        'labels': {'layer': lables_layer, 'datatype': 1},
        'chip': {'layer': chip_layer, 'datatype': 1}
    }

    ## SAVE FULL MASK IN DIC FOR EASY REFERENCING
    full_mask = {}
    for layer in layer_data.keys():
        full_mask[layer] = lib.new_cell(layer)
        
    layer_data_reversed = {}
    for k, v in layer_data.items():
        layer_data_reversed[v['layer']] = k
        
        
    chip_size_x = 8000
    chip_size_y = 10000
    # full_mask['chip'].add(create_rectangle('chip', 0, 0, chip_size_x, chip_size_y, layer_data))
    
    grating_x_offset = 0
    grating_y_offset = 0
    
    grating_radius = 4

    grating_period = 0.26
    grating_duty_cycle = 0.5
    
    theta = 0
    
    distance_between_gratings_x = grating_radius*6
    distance_between_gratings_y = grating_radius*6
    number_of_gratings_x = 40
    # number_of_gratings_x = 1
    number_of_gratings_y = int(distance_between_gratings_x/grating_radius)*4
    
    for i in range(number_of_gratings_x):
        for j in range(number_of_gratings_y):
            grating_x = i*distance_between_gratings_x + j*grating_radius + grating_x_offset
            grating_y = j*distance_between_gratings_y + grating_y_offset
            
            add_grating_and_mode_filter(grating_x, grating_y, grating_radius, grating_period, grating_duty_cycle, theta, full_mask, layer_data, circle_tolerance)
        
    labels_x = grating_x_offset - 400
    labels_y = grating_y_offset + 250
    
    label_polygon = create_mask_label(labels_x, labels_y, str(round(grating_duty_cycle, 2)), layer_data['labels'])
    
    for polygon in label_polygon:
        full_mask['labels'].add(polygon)
        
    # grating_x_offset = 1600
    # grating_y_offset = 0
    
    # grating_radius = 4

    # grating_period = 0.26
    # grating_duty_cycle = 0.55
    
    # distance_between_gratings_x = grating_radius*6
    # distance_between_gratings_y = grating_radius*6
    # number_of_gratings_x = 40
    # number_of_gratings_y = int(distance_between_gratings_x/grating_radius)*4

    
    # for i in range(number_of_gratings_x):
    #     for j in range(number_of_gratings_y):
    #         grating_x = i*distance_between_gratings_x + j*grating_radius + grating_x_offset
    #         grating_y = j*distance_between_gratings_y + grating_y_offset
            
    #         add_grating_and_mode_filter(grating_x, grating_y, grating_radius, grating_period, grating_duty_cycle, theta, full_mask, layer_data, circle_tolerance)
        
    # labels_x = grating_x_offset - 400
    # labels_y = grating_y_offset + 250
    
    # label_polygon = create_mask_label(labels_x, labels_y, str(round(grating_duty_cycle, 2)), layer_data['labels'])
    
    # for polygon in label_polygon:
    #     full_mask['labels'].add(polygon)
        
    # grating_x_offset = 3200
    # grating_y_offset = 0
    
    # grating_radius = 4

    # grating_period = 0.26
    # grating_duty_cycle = 0.6
    
    # distance_between_gratings_x = grating_radius*6
    # distance_between_gratings_y = grating_radius*6
    # number_of_gratings_x = 40
    # number_of_gratings_y = int(distance_between_gratings_x/grating_radius)*4
    
    # for i in range(number_of_gratings_x):
    #     for j in range(number_of_gratings_y):
    #         grating_x = i*distance_between_gratings_x + j*grating_radius + grating_x_offset
    #         grating_y = j*distance_between_gratings_y + grating_y_offset
            
    #         add_grating_and_mode_filter(grating_x, grating_y, grating_radius, grating_period, grating_duty_cycle, theta, full_mask, layer_data, circle_tolerance)
        
    # labels_x = grating_x_offset - 400
    # labels_y = grating_y_offset + 250
    
    # label_polygon = create_mask_label(labels_x, labels_y, str(round(grating_duty_cycle, 2)), layer_data['labels'])
    
    # for polygon in label_polygon:
    #     full_mask['labels'].add(polygon)
    
        
    
    ## ADD ALL CREATED CELLS TO MAIN LAYER
    for layer in full_mask.keys():
        cell_layer = gdstk.Reference(full_mask[layer])
        mask.add(cell_layer)

    ## CREATE FOLDER FOR MASKS
    mask_folder = 'MASKS'
    mask_folder_path = Path.joinpath(SELMA_path, mask_folder)
    if not os.path.exists(str(mask_folder_path)):
        os.makedirs(str(mask_folder_path))
        
        
    ## SAVE THE GENERATED MASK
    if save_layout:
        gds_file_name = mask_name + '.gds'
        save_mask_path = Path.joinpath(mask_folder_path, gds_file_name)
        lib.write_gds(str(save_mask_path))
        
        
        
if  __name__ == '__main__':
    main()

        