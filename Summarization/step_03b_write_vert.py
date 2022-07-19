from multiprocessing import Pool
import sys
from matplotlib import image as mpimg
import numpy as np
import os

from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def function(cropped_dir):
    sys.stdout.flush()
    print('working on', cropped_dir)
    sys.stdout.flush()
    input_filename = os.path.join(cropped_dir, 'image.tif')
    vert_filename = os.path.join(cropped_dir, 'vert.txt')

    image = mpimg.imread(input_filename)
    nx, ny = image.shape

    print('writing vert file')
    with open(vert_filename, 'w') as vert_file:
        for j in range(ny):
            for i in range(nx):
                vert_file.write(str(i) + ' ' + str(j) + ' ' + str(image[i, j]) + '\n')
        vert_file.close()

    print(nx, ny)


THREADS = 6
DIPHA_CONST = 8067171840
DIPHA_IMAGE_TYPE_CONST = 1
DIM = 2

input_dir = sys.argv[1]

cropped_image_dirs = [os.path.join(input_dir, listing) for listing in os.listdir(input_dir)]
cropped_image_dirs.sort()

pool = Pool(THREADS)
pool.map(function, cropped_image_dirs)
