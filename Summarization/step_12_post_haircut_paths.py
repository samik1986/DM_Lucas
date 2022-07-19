import sys
import os
from multiprocessing import Pool


def function(image_filename):
    print('working on', image_filename)
    image_output_dir = os.path.join(input_dir, os.path.splitext(image_filename)[0]) \
                       + '/' + ve_persistence_threshold + '_' + et_persistence_threshold + '/'
    command = './post-haircutpaths/a.out ' + image_output_dir
    os.system(command)


THREADS = 64
input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

pool = Pool(THREADS)
pool.map(function, image_filenames)
