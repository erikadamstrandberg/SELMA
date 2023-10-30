#%%

import os 
import numpy as np
# import gdstk 
from pathlib import Path
import cv2

import gdsfactory as gf

SELMA_path = Path(__file__).parent.resolve()
   
def create_rectangle(x, y, x_size, y_size, layer):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer)

def create_circle(key, x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius, 
                        layer=layer_data[key]['layer'],
                        datatype=layer_data[key]['datatype'],
                        tolerance=tolerance
                        )

def main():
    ## SETUP VARIABLES ##
    
    mask_name   = 'ANDREAS_GIFT'
    
    # # Name of ANDREAS_GIFT
    # cell_name   = 'ANDREAS_GIFT'
    
    save_layout = True
    
    # Set units and precision for layout
    # unit      = 1.0e-6
    # precision = 1.0e-10
    
    ## CREATE THE MASK ##
    # The GDSII file is called a library, which contains multiple cells.
    # lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
    # gdstk.Library()
    
    ## MAIN CELL
    TOP_CELL = gf.Component('TOP_CELL')
    
    ## LAYER DATA
    # ruler_layer = 2
    # lables_layer = 3
    # chip_layer = 1
    
    # layer_data = {
    #     'mask': {'layer': ruler_layer, 'datatype': 1},
    #     'chip': {'layer': chip_layer, 'datatype': 1}
    # }

    ## SAVE FULL MASK IN DIC FOR EASY REFERENCING
    # full_mask = {}
    # for layer in layer_data.keys():
    #     full_mask[layer] = lib.new_cell(layer)
        
    # layer_data_reversed = {}    
    # for k, v in layer_data.items():
    #     layer_data_reversed[v['layer']] = k
        
    images_folder = 'binary_images/andreas' 
    images_folder = Path.joinpath(SELMA_path, images_folder)
    images = os.listdir(str(images_folder))
    
    chosen_image = images[2]
    chosen_image_path = Path.joinpath(images_folder, chosen_image)
    
    img = cv2.imread(str(chosen_image_path), cv2.IMREAD_GRAYSCALE) 
    x_pixels = img.shape[0]
    y_pixels = img.shape[1]
    
    pixel_size = 70
    
    x = np.arange(0, x_pixels, 1)*pixel_size
    y = np.arange(0, y_pixels, 1)*pixel_size
    
    pixel_c = gf.components.rectangle((pixel_size, pixel_size), layer=(1,0))
    # polygons_in_grid = []
    for i in range(len(x)):
        for j in range(len(y)):
            if img[i][j] > 0.1:
                pixel_r = TOP_CELL.add_ref(pixel_c).translate(x[i], y[j]) 
                # polygons_in_grid.append(create_rectangle(
                #     x[i], y[j], pixel_size, pixel_size, 1))
    
    
    # for polygon in polygons_in_grid:
    #     full_mask['mask'].add(polygon)
        
    # ## Add circle
    # chip_circle = create_circle('chip', 76200+13795-2621, 76200+28440-91, 76200, layer_data, 0.0001)
    # full_mask['chip'].add(chip_circle)
    
    ## ADD ALL CREATED CELLS TO MAIN LAYER
    # for layer in full_mask.keys():
    #     cell_layer = gdstk.Reference(full_mask[layer])
    #     mask.add(cell_layer)

    ## CREATE FOLDER FOR MASKS
    mask_folder = 'MASKS'
    mask_folder_path = Path.joinpath(SELMA_path, mask_folder)
    if not os.path.exists(str(mask_folder_path)):
        os.makedirs(str(mask_folder_path))
        
    ## SAVE THE GENERATED MASK
    if save_layout:
        gds_file_name = mask_name + '.gds'
        save_mask_path = Path.joinpath(mask_folder_path, gds_file_name)
        TOP_CELL.write_gds(save_mask_path)
        
if  __name__ == '__main__':
    main()

        