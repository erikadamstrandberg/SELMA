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

lam0 = 976e-9
theta_t = 1
derivative_phase_gradient = 2*np.pi*np.sin(theta_t*np.pi/180)/lam0

dx = 260.4e-9
# x_grid = np.arange(0, 100e-6, dx)
x_grid = np.arange(0, 10*dx, dx)
y_grid = x_grid
phase_gradient = x_grid*derivative_phase_gradient % 2*np.pi

phase_gradient_map = np.zeros(shape=(len(x_grid), len(y_grid)))

for i in range(len(x_grid)):
    for j in range(len(y_grid)):
        phase_gradient_map[i, j] = phase_gradient[i]


plt.plot(x_grid, phase_gradient)
# plt.figure(1)
# plt.imshow(phase_gradient_map)

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
# cell_name = 'CGAN_deflector_v3_300um'
cell_name = 'CGAN_deflector_for_niclas'
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

dx = 210 + 2*25.2
dy = dx

for ii in range(len(x_grid)):
    if ii % 10 == 0:
        now = datetime.now()
        print('Running row: ' + str(ii) + '/' + str(len(x_grid)) + '. Time completed: ' + now.strftime("%H:%M:%S"))
        
    for jj in range(len(y_grid)):
        x_pos = ii*dx
        y_pos = jj*dy
        current_phase = phase_gradient_map[ii, jj]
        
        closest_phase_index = np.argmin(np.abs(current_phase - phase_list))
        
        grid = np.loadtxt(grid_folder + '\\' + grid_list[closest_phase_index])
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
    

