from multiprocessing import Pool
import sys
import os
import csv


def function(cube_dir):
    print('working on', cube_dir)
    dipha_edge_filename = os.path.join(cube_dir, 'dipha.edges')
    output_filename = os.path.join(cube_dir, 'dipha-edges.txt')
    os.system(
        "~/apps/MATLAB/R2021a/bin/matlab -nosplash -nodisplay -nodesktop -r \'load_persistence_diagram(\"" + dipha_edge_filename + "\",\"" + output_filename + "\"); quit;\'")


THREADS = 1

input_dir = sys.argv[1]
input_filename = sys.argv[2]

cube_dirs = []
with open(input_filename, 'r') as input_file:
    reader = csv.reader(input_file)
    for row in reader:
        cube_dirs.append(os.path.join(input_dir, row[0]) + '/')
    input_file.close()

print(len(cube_dirs), 'dirs')

#os.system('~/apps/MATLAB/R2021a/bin/matlab -nosplash -nodisplay -nodesktop -r')

pool = Pool(THREADS)
pool.map(function, cube_dirs)

