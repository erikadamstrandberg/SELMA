#%%

from pathlib import Path
import os

import numpy as np
import matplotlib.pyplot as plt

import gdstk
import re
from datetime import datetime

def create_rectangle(x, y, x_size, y_size, layer):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer)


project_folder = Path(__file__).parents[0]

#%%

grid_folder_name = 'zoned_lens'
grid_folder = str(project_folder) + '\\' + grid_folder_name
grid_list = os.listdir(grid_folder)
phase_list = []

for i in grid_list:
    match = re.search('(?<=PHASE_)(.*?)(?=.txt)', i)
    phase_list.append(float(match.group(0)))
    
phase_list = np.array(phase_list)

# Name of cell
cell_name = 'test_phases'
mask_name = cell_name
save_layout = True

mask_folder = Path(project_folder, cell_name)
if not os.path.exists(mask_folder):
    os.makedirs(mask_folder)

# Set units and precision for layout
unit = 1.0e-9
precision = 1.0e-10
circle_tolerance = 0.005


## CREATE THE MASK ##
# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
gdstk.Library()

# Main cell of mask
mask = lib.new_cell(cell_name)



x_pos = 0
y_pos = 0
current_phase = 3.1

closest_phase_index = np.argmin(np.abs(current_phase - phase_list))

choosen_grid = grid_folder + '\\' + grid_list[closest_phase_index]
print('Choosen grid: ' + choosen_grid)
grid = np.loadtxt(choosen_grid)
pixel_size = 2.1

x = np.arange(0, len(grid), 1)*pixel_size
y = np.arange(0, len(grid), 1)*pixel_size

x_size = pixel_size
y_size = pixel_size

polygons_in_grid = []

first = True
for i in range(len(x)):
    for j in range(len(y)):
        if grid[i][j] == 1:
            if first:
                CGAN_filled = create_rectangle(
                    x[i] + x_pos, y[j] + y_pos, x_size, y_size, 1)
                first = False
            else:
                  CGAN_filled = gdstk.boolean(CGAN_filled, create_rectangle(
                      x[i] + x_pos, y[j] + y_pos, x_size, y_size, 1), 'or')

precision = 0.0001
mask.add(CGAN_filled[0])
    
        

save_path = Path(mask_folder, mask_name)
lib.write_gds(str(save_path) + '.gds')
    

