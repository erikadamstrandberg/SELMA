#%%

from pathlib import Path
import os

import numpy as np
import matplotlib.pyplot as plt

import gdstk
import re
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def create_rectangle(x, y, x_size, y_size, layer):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer)


project_folder = Path(__file__).parents[0]

#%%

grid_folder_name = 'CGAN_metaatoms'
grid_folder = str(project_folder) + '\\' + grid_folder_name
grid_list = os.listdir(grid_folder)
phase_list = []

for i in grid_list:
    match = re.search('(?<=PHASE_)(.*?)(?=.txt)', i)
    phase_list.append(float(match.group(0)))
    
phase_list = np.array(phase_list)

# Name of cell
cell_name = 'timo_thesis'
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
grid_period = 260
pixel_size = 2.1

#%%

def phase_profile_lens_convex(lam0, f, r):
    return 2*np.pi*(f - np.sqrt(r**2 + f**2))/lam0 % 2*np.pi

grid_period = 260
x_size = 1
y_size = 1
x = np.arange(0, (x_size + 1)*grid_period, grid_period)
y = np.arange(0, (y_size + 1)*grid_period, grid_period)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

f = 100
phase_map = phase_profile_lens_convex(380e1, f, R)
plt.imshow(phase_map)


#%%

# phase_array = np.linspace(0, 2*np.pi, 15)
# phase_array = np.roll(phase_array, -2)

fig,ax = plt.subplots(1)
for ii in range(phase_map.shape[0]):
    for jj in range(phase_map.shape[1]):
        current_phase = phase_map[ii][jj]
        
        closest_phase_index = np.argmin(np.abs(current_phase - phase_list))
        print(closest_phase_index)
        choosen_grid = grid_folder + '\\' + grid_list[closest_phase_index]
        print('Choosen grid: ' + choosen_grid)
        grid = np.loadtxt(choosen_grid)
        
        x = np.arange(0, len(grid), 1)*pixel_size
        y = np.arange(0, len(grid), 1)*pixel_size
        
        x_size = pixel_size
        y_size = pixel_size
        
        first = True
        for i in range(len(x)):
            for j in range(len(y)):
                if grid[i][j] == 1:
                    rect1 = mpl.patches.Rectangle((x[i] + x_pos + ii*grid_period, y[j] + y_pos + jj*grid_period), pixel_size, pixel_size, fc='black')
                    ax.add_patch(rect1)
                
            
            
plt.xlim([0, grid_period*phase_map.shape[0]])
plt.ylim([0, grid_period*phase_map.shape[0]])
plt.axis('equal')
plt.tick_params(left = False, bottom = False) 
plt.axis('off')
    

