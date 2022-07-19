import sys
import os
from multiprocessing import Pool
import csv


def function(image_filename):
    print('working on', image_filename)
    image_output_dir = os.path.join(input_dir, os.path.splitext(image_filename)[0]) \
                       + '/' + ve_persistence_threshold + '_' + et_persistence_threshold + '/'
    input_filename = os.path.join(image_output_dir, 'dimo_edge.txt')
    output_filename = os.path.join(image_output_dir, 'no-dup-crossed-edge.txt')

    edges = set()
    with open(input_filename, 'r') as input_file:
        reader = csv.reader(input_file, delimiter=' ')
        for row in reader:
            v0 = int(row[0])
            v1 = int(row[1])
            if v0 < v1:
                vmin = v0
                vmax = v1
            else:
                vmin = v1
                vmax = v0
            if (vmin, vmax) not in edges:
                edges.add((vmin, vmax))
        input_file.close()

    with open(output_filename, 'w') as output_file:
        for e in edges:
            output_file.write(str(e[0]) + ' ' + str(e[1]) + '\n')
        output_file.close()


THREADS = 6
input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

pool = Pool(THREADS)
pool.map(function, image_filenames)
