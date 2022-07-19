import matplotlib
matplotlib.use('agg')

import os
import sys
import cv2
import numpy as np
import math
from matplotlib import image as mpimg
import scipy.misc

input_dir = sys.argv[1]
output_dir = sys.argv[2]
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

valid_filename = os.path.join(output_dir, 'valid-dirs.txt')

x_len = int(sys.argv[3])
y_len = int(sys.argv[4])
z_len = int(sys.argv[5])
overlap = int(sys.argv[6])

name_list = [name for name in os.listdir(input_dir) if
             (os.path.isfile(input_dir + '/' + name)) and (name != ".DS_Store")]
name_list.sort()

# mask_list = [os.path.join(mask_dir, name) for name in os.listdir(mask_dir)]

# assert(len(name_list) == len(mask_list))

im = mpimg.imread(input_dir + name_list[0])
nx, ny = im.shape
nz = len(name_list)


nx_cols = math.ceil(nx / x_len)
ny_cols = math.ceil(ny / y_len)
nz_cols = math.ceil(nz / z_len)

print(nx, ny, nz)

number_of_tiles = nx_cols * ny_cols * nz_cols
print('number of regions:', number_of_tiles, nx_cols, ny_cols, nz_cols)

del im

#im_cube = np.zeros([nx, ny, nz]

# im_cube = im_cube / 4095
# im_cube = im_cube * (2 ** 16)
'''
for i in range(len(image_list)):
    print(np.max(image_list[i]))
'''

valid_cubes = []
index = 0
for k in range(nz_cols):
    z_min = max(k * z_len, 0)
    z_max = min((k + 1) * z_len + overlap, nz)

    image_list = []
    # mask_image_list = []
    for z_slice in range(z_min, z_max):
        name = name_list[z_slice]
        # mask = mask_list[z_slice]
        fileName = input_dir + "/" + name
        image_list.append(mpimg.imread(fileName))
        # mask_image_list.append(mpimg.imread(mask))

    for j in range(ny_cols):
        for i in range(nx_cols):
            sys.stdout.flush()
            print('working on tile ', index, 'out of ', number_of_tiles)
            x_min = max(i * x_len, 0)
            x_max = min((i + 1) * x_len + overlap, nx)
            y_min = max(j * y_len, 0)
            y_max = min((j + 1) * y_len + overlap, ny)

            print(x_min, y_min, z_min, x_max, y_max, z_max)

            '''
            cube_mask = []
            for z_val in range(z_min, z_max):
                cube_mask.append(mask_image_list[z_val - z_min][x_min:x_max, y_min:y_max])
            cube_mask = np.asarray(cube_mask)
            '''

            cube = []
            for z_val in range(z_min, z_max):
                cube.append(image_list[z_val - z_min][x_min:x_max, y_min:y_max])

            if np.max(cube) == 0:
                print('skipping cube', index)
                index += 1
                continue

            tile_output_dir = output_dir + str(index) + '/'
            tile_image_output_dir = os.path.join(tile_output_dir, 'images/')
            if not os.path.exists(tile_output_dir):
                os.mkdir(tile_output_dir)
            if not os.path.exists(tile_image_output_dir):
                os.mkdir(tile_image_output_dir)
            coord_filename = os.path.join(tile_output_dir, 'coords.txt')
            with open(coord_filename, 'w') as coord_file:
                coord_file.write(str(x_min) + ' ' + str(y_min) + ' ' + str(z_min) + '\n')
                coord_file.close()
            slice_numbers = z_max - z_min
            digits = len(str(slice_numbers))
            for n in range(slice_numbers):
                n_slice = cube[n]
                '''
                n_max = np.max(n_slice)
                if n_max > slive_max:
                    slive_max = n_max
                '''
                # print('slice :', n_slice)
                n_slice.astype('uint16')
                #scipy.misc.toimage(n_slice, cmin=0.0, cmax=1.0).save(tile_output_dir + str(n).zfill(digits) + '.tif')
                cv2.imwrite(tile_image_output_dir + str(n).zfill(digits) + '.tif', n_slice)
            # sys.exit()
            valid_cubes.append(index)
            index += 1

with open(valid_filename, 'w') as valid_file:
    for v in valid_cubes:
        valid_file.write(str(v) + '\n')
    valid_file.close()
