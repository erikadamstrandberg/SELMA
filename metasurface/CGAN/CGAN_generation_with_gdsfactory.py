#%%

from pathlib import Path
import os
import re

import gdsfactory as gf
import numpy as np
import matplotlib.pyplot as plt

project_folder = Path(__file__).parents[0]

NM = 1e-6

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

grid_folder_name = 'zoned_lens'
save_gds_folder = 'zoned_lens_gds'
grid_folder = str(project_folder) + '\\' + grid_folder_name
save_gds_folder_path = str(project_folder) + '\\' + save_gds_folder

grid_list = os.listdir(grid_folder)
phase_list = []

for i in grid_list:
    match = re.search('(?<=PHASE_)(.*?)(?=.txt)', i)
    phase_list.append(float(match.group(0)))
    
phase_list = np.array(phase_list)

pixel_size = 2.1

x_pos = 0
y_pos = 0
current_phase = 6

closest_phase_index = np.argmin(np.abs(current_phase - phase_list))

choosen_grid = grid_folder + '\\' + grid_list[closest_phase_index]

# layout = gf.Layout(unit=1e-9)

meta_surface = gf.Component(grid_list[closest_phase_index].removesuffix('.txt'), unit=NM, grid=2.1)
# layout.add_ref(meta_surface)


# print(meta_surface.hash_geometry(precision=1e-4))

print('Choosen grid: ' + choosen_grid)
grid = np.loadtxt(choosen_grid)

x = np.arange(0, len(grid), 1)*pixel_size
y = np.arange(0, len(grid), 1)*pixel_size

polygons_in_grid = []

first = True
for i in range(len(x)):
    for j in range(len(y)):
        if grid[i][j] == 1:
            
            if first == True:
                metaatom_full = gf.components.rectangle(size=[pixel_size, pixel_size], layer=(0, 0))
                metaatom_full_ref = metaatom_full.ref()
                metaatom_full_ref.move([-x[i] + x_pos, y[j] + y_pos])
                first = False
                
            else:
                metaatom_added = gf.components.rectangle(size=[pixel_size, pixel_size], layer=(0, 0))
                metaatom_added_ref = metaatom_added.ref()
                metaatom_added_ref.move([-x[i] + x_pos, y[j] + y_pos])
                gf.geometry.boolean(A=metaatom_full, B=metaatom_added, operation='or')
                
                # metaatom_ref = meta_surface.add_ref(pixel_component)
                # metaatom_ref.move([-x[i] + x_pos, y[j] + y_pos])


meta_surface.add_ref(metaatom_full)

# print(metaatom_ref)

# meta_surface.show()
# save_path = Path(save_gds_folder_path, grid_list[closest_phase_index].removesuffix('.txt'))
# meta_surface.write_gds(str(save_path) + '.gds', unit=NM)


#%%

component1 = gf.Component("Component1")
component2 = gf.Component("Component2")

# Add polygons to the components
component1.add_polygon([(0, 0), (0, 10), (10, 10), (10, 0)], layer=1)
component2.add_polygon([(5, 5), (5, 15), (15, 15), (15, 5)], layer=2)

merged_component = gf.geometry.boolean_klayout(component1.ref(), component2.ref())