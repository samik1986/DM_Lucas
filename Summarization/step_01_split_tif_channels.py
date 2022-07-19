from multiprocessing import Pool
import sys
from matplotlib import image as mpimg
import os
import cv2

from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def function(image_filename):
    print('working on', image_filename)
    input_path = os.path.join(input_dir, image_filename)
    image = mpimg.imread(input_path)
    red_channel = image[:, :, 2]
    green_channel = image[:, :, 1]
    red_output = os.path.join(red_dir, image_filename)
    green_output = os.path.join(green_dir, image_filename)
    cv2.imwrite(red_output, red_channel)
    cv2.imwrite(green_output, green_channel)


THREADS = 64

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

red_dir = os.path.join(output_dir, 'red/')
if not os.path.exists(red_dir):
    os.mkdir(red_dir)

green_dir = os.path.join(output_dir, 'green/')
if not os.path.exists(green_dir):
    os.mkdir(green_dir)

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

pool = Pool(THREADS)
pool.map(function, image_filenames)

