from multiprocessing import Pool
import sys
from matplotlib import image as mpimg
import numpy as np
import os


def function(cropped_dir):
    sys.stdout.flush()
    print('working on', cropped_dir)
    sys.stdout.flush()
    input_filename = os.path.join(cropped_dir, 'image.tif')
    dipha_output_filename = os.path.join(cropped_dir, 'dipha.input')
    os.system(
        "~/apps/MATLAB/R2021a/bin/matlab -nosplash -nodisplay -nodesktop -r \'save_image_data(\"" + input_filename + "\",\"" + dipha_output_filename + "\"); quit;\'")

THREADS = 6

input_dir = sys.argv[1]

cropped_image_dirs = [os.path.join(input_dir, listing) for listing in os.listdir(input_dir)]
cropped_image_dirs.sort()

pool = Pool(THREADS)
pool.map(function, cropped_image_dirs)
