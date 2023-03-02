#%%

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

grid_folder_name = 'zoned_lens'
grid_folder = str(project_folder) + '\\' + grid_folder_name

grid_list = os.listdir(grid_folder)

for grid_name in grid_list:

    grid = np.loadtxt(grid_folder + '\\' + grid_name)
    mask_name = grid_name.replace('.txt', '')
    mask_folder = grid_folder + '_gds\\'

    if not os.path.exists(mask_folder):
        os.makedirs(mask_folder)

    # Name of cell
    cell_name = grid_name
    save_layout = True

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
                        x[i], y[j], x_size, y_size, 1)
                    first = False
                else:
                     CGAN_filled = gdstk.boolean(CGAN_filled, create_rectangle(
                         x[i], y[j], x_size, y_size, 1), 'or')
                # polygons_in_grid.append(create_rectangle(
                #     x[i], y[j], x_size, y_size, 1))
                # mask.add(create_rectangle(x[i], y[j], x_size, y_size, 1))

    precision = 0.0001
    mask.add(CGAN_filled[0])
    
    # merged_grid = gdstk.boolean(
    #     polygons_in_grid[0], polygons_in_grid[1], 'or', layer=1, precision=precision)

    # for i in range(2, len(polygons_in_grid), 1):
    #     merged_grid = gdstk.boolean(
    #         merged_grid, polygons_in_grid[i], 'or', layer=1, precision=precision)

    # merged_grid = merged_grid[0]

    # points = merged_grid.points
    # end_point = points[-1]

    # curve = gdstk.Curve(end_point)

    # curve.segment(points)
    # control_poly = gdstk.Polygon(curve.points(), datatype=1)
    # curve = gdstk.Curve(end_point, tolerance=1e-2)
    # curve.bezier(points)

    # polygon = gdstk.Polygon(curve.points(), layer=2)

    # mask.add(polygon)
    lib.write_gds(mask_folder + mask_name + '.gds')
    
#%%

grid_folder_name = 'zoned_lens_blockify'
grid_folder = str(project_folder) + '\\' + grid_folder_name

grid_list = os.listdir(grid_folder)

grid_list = grid_list[0:1]

for grid_name in grid_list:

    grid_blockify = np.loadtxt(grid_folder + '\\' + grid_name, delimiter=',')
    mask_name = grid_name.replace('.csv', '')
    mask_folder = grid_folder + '_gds\\'

    if not os.path.exists(mask_folder):
        os.makedirs(mask_folder)


    # print(grid_blockify)
    # Name of cell
    cell_name = grid_name
    save_layout = True

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

    pixel_size = 2.1
    
    for i in range(len(grid_blockify)):
        print(grid_blockify[i])
        x1_blockify = grid_blockify[i][0]*pixel_size
        y1_blockify = grid_blockify[i][1]*pixel_size
        dx = grid_blockify[i][2]*pixel_size
        dy = grid_blockify[i][3]*pixel_size
        
        
        x1 = x1_blockify
        y1 = y1_blockify
        
        x2 = x1_blockify + dx
        y2 = y1_blockify
        
        x3 = x1_blockify + dx
        y3 = y1_blockify + dy
        
        x4 = x1_blockify
        y4 = y1_blockify + dy
        
        mask.add(gdstk.Polygon([(x1, y1),
                                (x2, y2),
                                (x3, y3),
                                (x4, y4)],
                                 layer=1))

    lib.write_gds(mask_folder + mask_name + '.gds')
    

