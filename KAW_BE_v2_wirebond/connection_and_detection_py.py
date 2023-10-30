#%%

from pathlib import Path
import os
import numpy as np
import gdstk


def create_rectangle(key, x, y, x_size, y_size, layer_data, rotation=0, rot_center=(0,0)):
    right_x = x + x_size/2
    left_x  = x - x_size/2
    
    upper_y = y + y_size/2
    lower_y = y - y_size/2
    
    polygon = gdstk.Polygon([(right_x, upper_y),
                             (right_x, lower_y),
                             (left_x,  lower_y),
                             (left_x,  upper_y)],
                            layer=layer_data[key]['layer'],
                            datatype=layer_data[key]['datatype']).rotate(rotation, center=rot_center)
    
    return polygon

def create_circle(key, x, y, radius, layer_data, tolerance):
    
    return gdstk.ellipse(np.array([x, y]), 
                        radius,
                        layer=layer_data[key]['layer'],
                        datatype=layer_data[key]['datatype'],
                        tolerance=tolerance
                        )
    
    
project_folder = Path(__file__).parents[0]

## Read channels
GDS_folder = 'GDS'
channel_mask = 'SPR_Sensor_v6_only_detection.gds'
channel_mask_path = Path(project_folder, GDS_folder)
channel_mask_path = Path(channel_mask_path, channel_mask)
channel_lib = gdstk.read_gds(str(channel_mask_path))
channel_cells = channel_lib.cells

VCSEL_square = channel_cells[2].polygons[0]
thick_lines = channel_cells[6].polygons[0]
thin_lines = channel_cells[7].polygons[0]

# Set units and precision for layout
unit = 1.0e-9
precision = 1.0e-10
circle_tolerance = 0.005

## LAYER DATA
slide_layer = 1
traces_layer = 2

layer_data = {
    'slide': {'layer': slide_layer, 'datatype': 1},
    'traces': {'layer': traces_layer, 'datatype': 1}
}

folder_name = 'connection_and_detection_v2'
cell_name = 'connection_and_detection_mask_v2'
mask_name = cell_name
save_layout = True

mask_folder = Path(project_folder, folder_name)
if not os.path.exists(mask_folder):
    os.makedirs(mask_folder)

# Set units and precision for layout
unit = 1.0e-6
precision = 1.0e-10
circle_tolerance = 0.005


## CREATE THE MASK ##
# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
gdstk.Library()

# Main cell of mask
mask = lib.new_cell(cell_name)
inverted_mask = []

microscope_slide_x = 23000
microscope_slide_y = 73000


mask_polygons = []

inverted_mask = create_rectangle('slide', 0, 0, microscope_slide_x, microscope_slide_y, layer_data)
mask_polygons.append(inverted_mask)

mask_polygons.append(VCSEL_square)

number_of_traces_half = 10

x_bond_pad_first_row = -3200
# x_bond_pad_first_row = -2500
y_bond_pad_first_row = 0
bond_pad_size = 70

x_bond_pad_second_row = -3400
# x_bond_pad_second_row = -2700
y_bond_pad_second_row = 70
bond_pad_size = 70

offset_x_bond_pad_trace_first_row = -1500
offset_x_bond_pad_trace_second_row = -1300

start_bond_traces = -3600

y_distance_between_traces = 180
x_size_trace = 8000
y_size_trace = 120

y_distance_side = 1500


list_of_bond_pad_x = np.zeros(shape=number_of_traces_half*2)
list_of_bond_pad_y = np.zeros(shape=number_of_traces_half*2)
for i in range(-number_of_traces_half//2, number_of_traces_half//2, 1):
    bond_pad = create_circle('traces', x_bond_pad_first_row, y_bond_pad_first_row + i*y_distance_between_traces, bond_pad_size, layer_data, circle_tolerance)    
    mask_polygons.append(bond_pad)
    
    list_of_bond_pad_x[2*i] = start_bond_traces 
    list_of_bond_pad_y[2*i] = y_bond_pad_first_row + i*y_distance_between_traces
    
    bond_pad = create_circle('traces', x_bond_pad_second_row, y_bond_pad_second_row + i*y_distance_between_traces, bond_pad_size, layer_data, circle_tolerance)    
    mask_polygons.append(bond_pad)
    
    list_of_bond_pad_x[2*i+1] = start_bond_traces
    list_of_bond_pad_y[2*i+1] = y_bond_pad_second_row + i*y_distance_between_traces+12

    
# number_of_thin_lines = 532
# x_start_thin_lines = 1400
# distance_between_thin_lines = 15

# for i in range(number_of_thin_lines):
#     thin_line_copy = thin_lines.copy().translate((x_start_thin_lines + i*distance_between_thin_lines, 0)) 
#     mask_polygons.append(thin_line_copy)

# number_of_thick_lines = 53
# x_start_thick_lines = 1400
# distance_between_thick_lines = 150

# for i in range(number_of_thick_lines):
#     thick_line_copy = thick_lines.copy().translate((x_start_thick_lines + i*distance_between_thick_lines, 0))
#     inverted_mask = gdstk.boolean(inverted_mask, thick_line_copy, 'not')   
#     mask_polygons.append(thick_line_copy)

number_of_solder_pads = number_of_traces_half*2
y_solder_pad = 0
x_solder_pad = -10000
solder_pad_size = 500
distance_between_solder_pads = 1500

list_of_solder_pad_x = np.zeros(shape=number_of_traces_half*2)
list_of_solder_pad_y = np.zeros(shape=number_of_traces_half*2)


for i in range(-number_of_solder_pads//2, number_of_solder_pads//2, 1):
    solder_pad = create_circle('traces', x_solder_pad, y_solder_pad + i*distance_between_solder_pads, solder_pad_size, layer_data, circle_tolerance)
    
    list_of_solder_pad_x[i] = x_solder_pad
    list_of_solder_pad_y[i] = y_solder_pad + i*distance_between_solder_pads
    
    mask_polygons.append(solder_pad)



for i in range(-number_of_traces_half, number_of_traces_half, 1):
    first_offset_x = list_of_bond_pad_x[i] + np.abs(i)*150 - 6500
    first_offset_y = list_of_bond_pad_y[i] + i*150
    
    
    path = gdstk.FlexPath(
        [(list_of_bond_pad_x[i], list_of_bond_pad_y[i])],
        [40],
        0,
        joins=['round'],
        ends=['flush'],
        layer=layer_data['traces']['layer'],
        datatype=layer_data['traces']['datatype'],
        tolerance=1e-3
    )
    
    
    first_x_between_bond_pads = list_of_bond_pad_x[i] + 200
    path.bezier(
    [(list_of_bond_pad_x[i], list_of_bond_pad_y[i]),
     (first_offset_x, first_offset_y),
     (first_offset_x, list_of_solder_pad_y[i]),
     (list_of_solder_pad_x[i], list_of_solder_pad_y[i])],
    width = 200,
    )
    
    mask_polygons.append(path)
    
    start_extentions_x = list_of_bond_pad_x[i] - 4
    start_extentions_y = list_of_bond_pad_y[i]
    
    if i%2 == 0:
        path = gdstk.FlexPath(
            [(start_extentions_x, start_extentions_y)],
            [40],
            0,
            joins=['round'],
            ends=['flush'],
            layer=layer_data['traces']['layer'],
            datatype=layer_data['traces']['datatype'],
            tolerance=1e-3
        )
        
        first_x_between_bond_pads = list_of_bond_pad_x[i] + 200
        crocked_path_x = list_of_bond_pad_x[i] + 200
        crocked_path_y = list_of_bond_pad_y[i] - 45
        path.bezier(
        [(start_extentions_x, start_extentions_y),
          (crocked_path_x, crocked_path_y),
          (list_of_bond_pad_x[i] + 400, list_of_bond_pad_y[i])],
        width = 2,
        )
        
    else:
        path = gdstk.FlexPath(
            [(start_extentions_x, start_extentions_y)],
            [40],
            0,
            joins=['round'],
            ends=['flush'],
            layer=layer_data['traces']['layer'],
            datatype=layer_data['traces']['datatype'],
            tolerance=1e-3
        )
        
        first_x_between_bond_pads = list_of_bond_pad_x[i] + 200
        path.bezier(
        [(start_extentions_x, start_extentions_y),
          (list_of_bond_pad_x[i]+200, list_of_bond_pad_y[i]-15)],
        width = 20,
        )
        
    
    mask_polygons.append(path)
    
    
    
## Changed to Klayout for boolean operations
# for i, path in enumerate(mask_polygons):
#     print('Cutting out: ' + str(i) + ' of ' + str(len(mask_polygons)))
#     inverted_mask = gdstk.boolean(inverted_mask, path, 'not')
             
    
# for polygon in inverted_mask:
#     print('Adding: ' + str(i) + ' of ' + str(len(mask_polygons)))
#     mask.add(polygon)

for polygon in mask_polygons:
    mask.add(polygon)
    
        

save_path = Path(mask_folder, cell_name)
lib.write_gds(str(save_path) + '.gds')
    

