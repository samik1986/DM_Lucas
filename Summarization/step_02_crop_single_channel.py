from multiprocessing import Pool
import sys
from matplotlib import image as mpimg
import os
import cv2
import numpy as np

from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def function(image_filename):
    print('working on', image_filename)
    input_filename = os.path.join(input_dir, image_filename)
    image_output_dir = os.path.join(output_dir, os.path.splitext(image_filename)[0]) + '/'
    # print(image_output_dir)
    crop_filename = os.path.join(image_output_dir, 'crop.txt')
    cropped_filename = os.path.join(image_output_dir, 'image.tif')
    # print(cropped_filename)

    if not os.path.exists(image_output_dir):
        os.mkdir(image_output_dir)

    image = mpimg.imread(input_filename)
    nx, ny = image.shape

    print('cropping')
    x, y = np.nonzero(image)
    xl, xr = x.min(), x.max()
    yl, yr = y.min(), y.max()
    cropped = image[xl - 1:xr + 2, yl - 1:yr + 2]

    cropped = image

    print('outputting')
    cv2.imwrite(cropped_filename, cropped)

    with open(crop_filename, 'w') as crop_file:
        crop_file.write(str(xl - 1) + ' ' + str(xr + 2) + ' ' + str(yl - 1) + ' ' + str(yr + 2) + '\n')
        crop_file.close()


THREADS = 64

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

image_filenames = [listing for listing in os.listdir(input_dir)]
pool = Pool(THREADS)
pool.map(function, image_filenames)
