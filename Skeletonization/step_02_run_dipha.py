from multiprocessing import Pool
import sys
import os
import csv


def function(directory):
    input_filename = 'dipha.input'
    diagram_filename = 'dipha.out'
    command = PATH_TO_DIPHA + ' --upper_dim 2 ' + os.path.join(directory, input_filename) + ' ' + os.path.join(directory, diagram_filename) + ' ' + os.path.join(directory, 'dipha.edges')
    os.system(command)
    command = 'rm ' + os.path.join(directory, input_filename)
    os.system(command)
    command = 'rm ' + os.path.join(directory, diagram_filename)
    os.system(command)


PATH_TO_DIPHA = '../../dipha-3d/build/dipha'
THREADS = 1

input_dir = sys.argv[1]
valid_dirs_filename = sys.argv[2]

print('reading dirs')
valid_dirs = []
with open(valid_dirs_filename, 'r') as valid_dirs_file:
    reader = csv.reader(valid_dirs_file, delimiter=' ')
    for row in reader:
        valid_dirs.append(row[0])
    valid_dirs_file.close()

dirs = [os.path.join(input_dir, v) + '/' for v in valid_dirs]

print('dipha time')
pool = Pool(THREADS)
results = pool.map(function, dirs)
pool.close()
pool.join()

