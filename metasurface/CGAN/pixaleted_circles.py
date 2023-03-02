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

#%%

def create_mask_label(x, y, text, layer_data):
    height = 10
    
    return gdstk.text(text, height,
                       (x, y),
                       layer=layer_data['layer'],
                       datatype=layer_data['datatype'])

def xy_source(r, seperation):
    x = np.arange(-r/2, r/2 + seperation, seperation) # Vektor med källpunkter i x-led
    y = x                                                       # och i y-led
    
    X, Y = np.meshgrid(x, y)                                    
    R    = np.sqrt(X**2 + Y**2)                                 # Längd från origo till källpunkter
    
    element_inuti_diameter = R < (r/2)                          # Element innan för D_star

    x = X[element_inuti_diameter]                               # Plock ut x-koordinater som är innanför D_star
    y = Y[element_inuti_diameter]                               # och plocka ut y-koordinater
    
    coordinates = []
    for i in range(len(x)):
        coordinates.append((x[i], y[i]))
    return coordinates

def add_pixalated_circle(r, pixel_side, x0, y0, layer_data, full_mask):
    coordinates = xy_source(r, pixel_side)    
    pixalated_circle_separated = []
    for i in range(len(coordinates)):
        x = coordinates[i][0]
        y = coordinates[i][1]
        
        single_pixel = gdstk.Polygon([(x + pixel_side, y + pixel_side),
                                      (x + pixel_side, y - pixel_side),
                                      (x - pixel_side, y - pixel_side),
                                      (x - pixel_side, y + pixel_side)])
        pixalated_circle_separated.append(single_pixel)
    pixalated_circle = pixalated_circle_separated[0]
        
    for i in range(1, len(pixalated_circle_separated)):
        pixalated_circle = gdstk.boolean(pixalated_circle, pixalated_circle_separated[i], 'or', 
                                         layer=layer_data['pixalated_circles']['layer'],
                                         datatype=layer_data['pixalated_circles']['datatype'])
        
        
    return pixalated_circle[0]
    
def create_square_of_pixalated_circles(r, pixel_side, x_offset, y_offset, number_atoms_x, number_atoms_y, dx_dy, layer_data, full_mask):
    x_array = np.arange(x_offset, x_offset + number_atoms_x*dx_dy, dx_dy)
    y_array = np.arange(y_offset, y_offset + number_atoms_y*dx_dy, dx_dy)
    
    pixalated_circle = add_pixalated_circle(r, pixel_side, x_array[0], y_array[0], layer_data, full_mask)
    full_mask['pixalated_circles'].add(pixalated_circle)
    
    for i in range(len(x_array)):
        for j in range(len(y_array)):
            pixalated_circle_copy_translated = pixalated_circle.copy().translate(x_array[i], y_array[j])
            full_mask['pixalated_circles'].add(pixalated_circle_copy_translated)
    

def main():
    ## SETUP VARIABLES ##
    
    mask_name   = 'CALIBRATION_MATRIX_v2'
    
    # Name of cell
    cell_name   = 'CALIBRATION_MATRIX_v2'
    
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
        'pixalated_circles': {'layer': pixalated_circles_layer, 'datatype': 1},
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
        
        
    full_mask['chip'].add(gdstk.rectangle((-4000, -4000), (4000, 4000)))
        
    r  = np.array([0.10, 0.14, 0.18, 0.22])
    pixel_side = np.array([0.002, 0.004, 0.006, 0.008, 0.014, 0.020])
    
    x_margin = 80
    y_margin = 80

    number_atoms_x = 200
    number_atoms_y = 400
    dx_dy = 0.270
    
    x_offset = 0
    y_offset = 0
    
    x_offset_label = -5
    y_offset_label = 120
    
    
    
    for i in range(len(r)):
        x_offset = x_offset + number_atoms_x*dx_dy + x_margin
        for j in range(len(pixel_side)):
            y_offset = y_offset + number_atoms_y*dx_dy + y_margin
            
            create_square_of_pixalated_circles(r[i], pixel_side[j], x_offset, y_offset,
                                                number_atoms_x, number_atoms_y, dx_dy, 
                                                layer_data, full_mask)
            
            print(pixel_side[j]*1000)
            label_string = 'r ' + str(round(r[i]*1000)) + '   ' + 'px ' + str(round(pixel_side[j]*1000))
            label = create_mask_label(x_offset + x_offset_label, y_offset + y_offset_label, label_string, layer_data['labels'])
            for k in range(len(label)):
                full_mask['labels'].add(label[k])
            
        y_offset = 0

        
        
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

        