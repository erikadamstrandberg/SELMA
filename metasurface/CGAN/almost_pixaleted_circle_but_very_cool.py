#%%

import os 

import numpy as np
import matplotlib.pyplot as plt

from scipy import constants
c     = constants.speed_of_light
mu_0  = constants.mu_0
eps_0 = constants.epsilon_0

import gdstk 


#%%

def create_mask_label(x, y, text, layer_data):
    height = 4
    
    return gdstk.text(text, height,
                       (x, y),
                       layer=layer_data['layer'],
                       datatype=layer_data['datatype'])

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
    nanopillars_layer = 1
    lables_layer = 2
    
    layer_data = {
        'pixalated_circles': {'layer': nanopillars_layer, 'datatype': 1},
        'labels': {'layer': lables_layer, 'datatype': 1}
    }

    ## SAVE FULL MASK IN DIC FOR EASY REFERENCING
    full_mask = {}
    for layer in layer_data.keys():
        full_mask[layer] = lib.new_cell(layer)
        
    layer_data_reversed = {}    
    for k, v in layer_data.items():
        layer_data_reversed[v['layer']] = k
        
        
    r  = 100
    y0 = 0
    x0 = 0
    seperation = 5
    
    tolerance = 5 
    offset = 5
    
    def xy_source(N, r, seperation):
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


    coordinates = xy_source(10, r, seperation)

    # print(coordinates)
    # plt.figure(1)
    # plt.plot(x, y, 'ro', markersize=1.4)
    # plt.axis('equal')
    
    
    rect = gdstk.Polygon(coordinates)
    full_mask['pixalated_circles'].add(rect)
        
        
    ## ADD ALL CREATED CELLS TO MAIN LAYER
    for layer in full_mask.keys():
        cell_layer = gdstk.Reference(full_mask[layer])
        mask.add(cell_layer)

    ## CREATE FOLDER FOR MASKS
    mask_folder = 'MASKS/'
    if not os.path.exists(mask_folder):
        os.makedirs(mask_folder)
        
        
    ## SAVE THE GENERATED MASK
    if save_layout:
        lib.write_gds(mask_folder + mask_name + '.gds')
        
if  __name__ == '__main__':
    main()

        