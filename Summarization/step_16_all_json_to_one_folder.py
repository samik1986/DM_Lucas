from multiprocessing import Pool
import sys
import os
from shutil import copyfile


def function(image_filename):
    print('working on', image_filename)
    image_output_dir = os.path.join(input_dir, os.path.splitext(image_filename)[0]) \
                       + '/' + ve_persistence_threshold + '_' + et_persistence_threshold + '/'

    json_filename = os.path.join(image_output_dir, 'GeoJson/0000.json')

    output_filename = os.path.join(output_dir, os.path.splitext(image_filename)[0] + '.json')
    copyfile(json_filename, output_filename)


THREADS = 32

input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]
output_dir = sys.argv[4]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

pool = Pool(THREADS)
pool.map(function, image_filenames)
