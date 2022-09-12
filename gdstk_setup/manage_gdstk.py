#%%

import gdstk
import os
import sys
from pathlib import Path

project_folder = Path(__file__).parents[1]
shapes_folder = str(Path(project_folder,'shapes'))

if shapes_folder not in sys.path:
    sys.path.append(shapes_folder)
    
from generic_shapes import create_polygon, create_rectangle, create_circle, create_annulus, create_half_annulus
from vcsel_chip_shapes import create_a_marks_all_layers, create_initial_a_marks_all_layers, create_orientation_arrow, create_TLM_circles, create_TLM_pads, create_label, create_all_labels



class chip_mask:
    def __init__(self, mask_dict, mask_cell, layer_data, layer_data_reversed, gds_lib,  circle_tolerance):
        self.mask_dict = mask_dict
        self.mask_cell = mask_cell
        self.layer_data = layer_data
        self.layer_data_reversed = layer_data_reversed
        self.gds_lib = gds_lib
        self.circle_tolerance = circle_tolerance
        
        
        
        
    ##### Generic shapes #####
    def create_polygon(self, key, x1, y1, x2, y2, x3, y3, x4, y4, layer_data, rotation=0):
        self.mask_dict[key].append(create_polygon(key,
                                                  x1, y1,
                                                  x2, y2,
                                                  x3, y3,
                                                  x4, y4,
                                                  self.layer_data, rotation=0))
        
        
    def create_rectangle(self, key, x, y, x_size, y_size, rotation=0):
        self.mask_dict[key].append(create_rectangle(key, x, y, 
                                                    x_size, y_size, 
                                                    self.layer_data, 
                                                    rotation=rotation
                                                    ))
        
    def create_circle(self, key, x, y, radius):
        self.mask_dict[key].append(create_circle(key, x, y, 
                                                 radius, 
                                                 self.layer_data,
                                                 self.circle_tolerance
                                                 ))
        
    def create_annulus(self, key, x, y, inner, outer):
        self.mask_dict[key].append(create_annulus(key, x, y,
                                                  inner, outer,
                                                  self.layer_data,
                                                  self.circle_tolerance
                                                  ))
        
    def create_half_annulus(self, key, x, y, inner, outer, initial_angle, final_angle):
        self.mask_dict[key].append(create_half_annulus(key, x, y,
                                                       inner, outer,
                                                       initial_angle, final_angle,
                                                       self.layer_data, 
                                                       self.circle_tolerance
                                                       ))
        
        
    ##### VCSEL shapes #####
    def create_initial_a_marks_all_layers(self, frame_size_x, frame_size_y, colums_of_alignment_marks):
        alignment_polygons = create_initial_a_marks_all_layers(frame_size_x, frame_size_y,
                                                       colums_of_alignment_marks,
                                                       self.layer_data)
        
        for polygons in alignment_polygons:
            for polygon in polygons:
                self.find_layer_key_and_add(polygon)
                
                
    def create_a_marks_all_layers(self, chip_size_x, chip_size_y,
                                  frame_size_x, frame_size_y,
                                  colums_of_alignment_marks, aligment_mark_offset):
        
        (DD_alignment_polygons, cover_DD_polygons, DC_alignment_polygons, cover_DC_polygons) = create_a_marks_all_layers(chip_size_x, chip_size_y,
                                                                                                                         frame_size_x, frame_size_y,
                                                                                                                         colums_of_alignment_marks, aligment_mark_offset, 
                                                                                                                         self.layer_data)
        for polygons in DD_alignment_polygons:
            for polygon in polygons:
                self.find_layer_key_and_add(polygon)
                
        for polygons in cover_DD_polygons:
            self.find_layer_key_and_add(polygons)
            
        for polygons in DC_alignment_polygons:
            for polygon in polygons:
                self.find_layer_key_and_add(polygon)
                
        for polygons in cover_DC_polygons:
            self.find_layer_key_and_add(polygons)
                
    def create_orientation_arrow(self, key, x, y, arrow_head, arrow_base):
        self.mask_dict[key].append(create_orientation_arrow(key, x, y, arrow_head, arrow_base, self.layer_data))
        
        
        
    def create_TLM_circles(self, ring_layer, x, y):
        TLM_circles = create_TLM_circles(ring_layer, x, y, self.layer_data, self.circle_tolerance)
        
        self.find_layer_key_and_add(TLM_circles)
            
        
        
    def create_TLM_pads(self, pad_layer, x, y):
        TLM_pads = create_TLM_pads(pad_layer, x, y, self.layer_data)
        
        self.find_layer_key_and_add(TLM_pads)
            
        
    def create_label(self, key, x, y, size, text):
        label_polygons = create_label(key, x, y, size, text, self.layer_data)
        
        self.find_layer_key_and_add(label_polygons)
        
    def create_all_labels(self, x, y, label_distance_y):
        label_polygons = create_all_labels(x, y, label_distance_y, self.layer_data)
        
        for label_list in label_polygons:
            self.find_layer_key_and_add(label_list)
            
    def add_polygon(self, key, polygon):
        self.mask_dict[key].append(polygon)
            
    def add_polygon_list(self, key, polygons):
        for polygon in polygons:
            self.mask_dict[key].append(polygon)
        

    def find_layer_key_and_add(self, polygon_list):
        for label in polygon_list:
            key = self.layer_data_reversed[label.layer]
            self.mask_dict[key].append(label)
    



def setup_gds_lib(mask_name, cell_name, layer_data):
    # Set units and precision for layout
    unit      = 1.0e-6
    precision = 1.0e-10
    circle_tolerance = 0.005
    
    ## CREATE THE MASK ##
    # The GDSII file is called a library, which contains multiple cells.
    gds_lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
    gdstk.Library()
    
    # Main cell of mask
    mask_cell = gds_lib.new_cell(cell_name)
    
    layer_data_reversed = {}    
    for k, v in layer_data.items():
        layer_data_reversed[v['layer_number']] = k
        
    mask_dict = {}
    
    for layer in layer_data.keys():
        mask_dict[layer] = [gds_lib.new_cell(layer)]
        
    return chip_mask(mask_dict, mask_cell, layer_data, layer_data_reversed, gds_lib,  circle_tolerance)
    



def save_gds_file(chip_mask, mask_name, mask_folder, save_layout):
    created_mask_folder =  str(mask_folder) + '\\mask\\'
    
    ### Add cell to main layer
    for layer in chip_mask.mask_dict.keys():
        for cells in chip_mask.mask_dict[layer]:
            if type(cells) == gdstk.Polygon:
                chip_mask.mask_cell.add(cells)
                
                ######  Make work for smaller output! ######
                # cell_layer = gdstk.Reference(full_mask[layer])
                # print(gdstk.Reference(full_mask[layer]))
        
    # Save the library in a file called 'first.gds'.
    if save_layout:
        chip_mask.gds_lib.write_gds(created_mask_folder + mask_name + '.gds')
        
def create_folder_for_mask(mask_folder):
    created_mask_folder =  str(mask_folder) + '\\mask\\'
        
    if not os.path.exists(created_mask_folder):
        os.makedirs(created_mask_folder)