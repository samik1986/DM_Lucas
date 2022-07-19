from multiprocessing import Pool
import sys
import os


def function(cropped_dir):
    print('working on', cropped_dir)
    dipha_edge_filename = os.path.join(cropped_dir, 'dipha-thresh.edges')
    dimo_input_filename = os.path.join(cropped_dir, 'dipha-edges.txt')
    matlab_command = MATLAB_PATH + " -r 'load_persistence_diagram(" + '"' + dipha_edge_filename + '", "' + dimo_input_filename + '"); exit;' + "'"
    os.system(matlab_command)


THREADS = 1
MATLAB_PATH = '~/apps/MATLAB/R2021a/bin/matlab'

input_dir = sys.argv[1]
cropped_image_dirs = [os.path.join(input_dir, listing) for listing in os.listdir(input_dir)]
cropped_image_dirs.sort()

pool = Pool(THREADS)
pool.map(function, cropped_image_dirs)
