# %%

from pathlib import Path
import numpy as np
import os

import gdstk

def create_rectangle(x, y, x_size, y_size, layer):
    return gdstk.Polygon([(x + x_size/2, y + y_size/2),
                          (x + x_size/2, y - y_size/2),
                          (x - x_size/2, y - y_size/2),
                          (x - x_size/2, y + y_size/2)],
                         layer=layer)


project_folder = Path(__file__).parents[0]

grid_folder_name = 'lens_grids'
grid_folder = str(project_folder) + '\\' + grid_folder_name

grid_list = os.listdir(grid_folder)

mask_folder = str(project_folder) + '\\' + 'CGAN_lens_v1\\'

if not os.path.exists(mask_folder):
    os.makedirs(mask_folder)
    
def phase_profile_lens_convex(lam0, f, r):
    return 2*np.pi*(f - np.sqrt(r**2 + f**2))/lam0 % 2*np.pi


phase_profile_discretazation = 10000
lens_radius = 200e-6
r = np.linspace(0, lens_radius, phase_profile_discretazation)
f = 6e-3
lam0 = 980e-9

#%%
# Name of cell
cell_name = 'CGAN_zoned_lens_v1'
mask_name = cell_name
save_layout = True

# Set units and precision for layout
unit = 1.0e-9
precision = 1.0e-10
circle_tolerance = 0.005


grid_list = grid_list[0:10]


## CREATE THE MASK ##
# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library(name=mask_name, unit=unit, precision=precision)
gdstk.Library()

# Main cell of mask
mask = lib.new_cell(cell_name)

dx = 280
dy = dx
discretazation = 100

grid_counter_x = 0
grid_counter_y = 0

num_colums = 11
num_metaatoms_x = 30
num_metaatoms_y = 30

for grid_name in grid_list:
    
    grid = np.loadtxt(grid_folder + '\\' + grid_name)
    pixel_size = 2.1

    x = np.arange(0, len(grid), 1)*pixel_size
    y = np.arange(0, len(grid), 1)*pixel_size

    x_size = pixel_size
    y_size = pixel_size
    polygons_in_grid = []
    
    for i in range(len(x)):
        for j in range(len(y)):
            if grid[i][j] == 1:
                polygons_in_grid.append(create_rectangle(
                    x[i], y[j], x_size, y_size, 1))

    merged_grid = gdstk.boolean(
        polygons_in_grid[0], polygons_in_grid[1], 'or', layer=1, precision=precision)

    for i in range(2, len(polygons_in_grid), 1):
        merged_grid = gdstk.boolean(
            merged_grid, polygons_in_grid[i], 'or', layer=1, precision=precision)

    merged_grid = merged_grid[0]

    points = merged_grid.points
    end_point = points[-1]

    curve = gdstk.Curve(end_point)

    curve.segment(points)
    control_poly = gdstk.Polygon(curve.points(), datatype=1)
    curve = gdstk.Curve(end_point, tolerance=1e-2)
    curve.bezier(points)

    polygon = gdstk.Polygon(curve.points(), layer=2)
            
    for i in range(num_metaatoms_x):
        x_offset = i*dx + grid_counter_x*dx*num_metaatoms_x
        
        for j in range(num_metaatoms_y):
            y_offset = j*dy + grid_counter_y*dy*num_metaatoms_y
            
            copy = polygon.copy()
            copy.translate(x_offset, y_offset)
            mask.add(copy)
            
    grid_counter_x += 1
    
    if grid_counter_x == num_colums:
        grid_counter_x = 0
        grid_counter_y += 1
        print('new row')



precision = 0.0001

lib.write_gds(mask_folder + mask_name + '.gds')
