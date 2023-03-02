# %%

from pathlib import Path
import numpy as np
import os

import gdstk
from matplotlib import pyplot as plt

def create_rectangle(x, y, x_size, y_size, layer):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer)


project_folder = Path(__file__).parents[0]

grid_folder_name = 'zoned_lens'
grid_folder = str(project_folder) + '\\' + grid_folder_name

grid_list = os.listdir(grid_folder)

mask_folder = str(project_folder) + '\\' + 'CGAN_zoned_lens_v1\\'

if not os.path.exists(mask_folder):
    os.makedirs(mask_folder)
    
def phase_profile_lens_convex(lam0, f, r):
    return 2*np.pi*(f - np.sqrt(r**2 + f**2))/lam0 % 2*np.pi


phase_profile_discretazation = 10000
lens_radius = 200e-6
# lens_radius = 1e-9
# r = np.linspace(0, lens_radius, phase_profile_discretazation)
# f = 6e-3
f = 1e-4
lam0 = 980e-9

dx_dy = 280e-9
# extent = 100e-6
extent = dx_dy*40

x = np.arange(-extent, extent, dx_dy)
y = x
X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2)

phase_profile_2d = phase_profile_lens_convex(lam0, f, R)

plt.imshow(phase_profile_2d)
# Name of cell
cell_name = 'CGAN_zoned_lens_v1'
mask_name = cell_name
save_layout = True

# Set units and precision for layout
unit = 1.0e-9
precision = 1.0e-10
circle_tolerance = 0.005

grid_phase = np.zeros(len(grid_list))

for i in range(len(grid_list)):
    grid_phase[i] = grid_list[i].split('_')[3].replace('.txt', '')
    
#%%

## CREATE THE MASK ##
# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
gdstk.Library()

# Main cell of mask
mask = lib.new_cell(cell_name)

for i in range(len(R)):
    print(i)
    for j in range(len(R)):
        print(j)
        
        x_current = X[i, j]*1e9
        y_current = Y[i, j]*1e9
        needed_phase = phase_profile_2d[i, j]
        
        index_selected_phase = np.argmin(np.abs(needed_phase - grid_phase))
        selected_metaatom = grid_list[index_selected_phase]
        
        grid = np.loadtxt(grid_folder + '\\' + selected_metaatom)
        pixel_size = 2.1

        x = np.arange(0, len(grid), 1)*pixel_size
        y = np.arange(0, len(grid), 1)*pixel_size
        
        x_size = pixel_size
        y_size = pixel_size
        polygons_in_grid = []
        
        for k in range(len(x)):
            for u in range(len(y)):
                if grid[k][u] == 1:
                    polygons_in_grid.append(create_rectangle(
                        x[k], y[u], x_size, y_size, 1))

        merged_grid = gdstk.boolean(
            polygons_in_grid[0], polygons_in_grid[1], 'or', layer=1, precision=precision)

        for k in range(2, len(polygons_in_grid), 1):
            merged_grid = gdstk.boolean(
                merged_grid, polygons_in_grid[k], 'or', layer=1, precision=precision)

        merged_grid = merged_grid[0]

        points = merged_grid.points
        end_point = points[-1]

        curve = gdstk.Curve(end_point)

        curve.segment(points)
        control_poly = gdstk.Polygon(curve.points(), datatype=1)
        curve = gdstk.Curve(end_point, tolerance=1e-2)
        curve.bezier(points)

        polygon = gdstk.Polygon(curve.points(), layer=2)
        polygon.translate(x_current, y_current)
        mask.add(polygon)
        
    

lib.write_gds(mask_folder + mask_name + '.gds')
