from multiprocessing import Pool
import sys
from matplotlib import image as mpimg
import os
import numpy as np
import csv

from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def function(image_filename):
    print('working on', image_filename)
    image_output_dir = os.path.join(input_dir, os.path.splitext(image_filename)[0]) \
                       + '/' + ve_persistence_threshold + '_' + et_persistence_threshold + '/'
    binary_process = os.path.join(binary_dir, image_filename + '.tif')

    vert_filename = os.path.join(image_output_dir, 'uncropped_dimo_vert.txt')
    edge_filename = os.path.join(image_output_dir, 'dimo_edge.txt')

    crossed_vert_filename = os.path.join(image_output_dir, 'crossed-vert.txt')
    crossed_edge_filename = os.path.join(image_output_dir, 'crossed-edge.txt')

    print('reading binary')
    binary = mpimg.imread(binary_process)

    print('reading verts')
    verts = []
    with open(vert_filename, 'r') as vert_file:
        reader = csv.reader(vert_file, delimiter=' ')
        for row in reader:
            verts.append([int(row[0]), int(row[1]), row[2]])
        vert_file.close()

    print('reading edges')
    edges = []
    with open(edge_filename, 'r') as edge_file:
        reader = csv.reader(edge_file, delimiter=' ')
        for row in reader:
            edges.append([int(row[0]), int(row[1])])
        edge_file.close()

    print('checking included verts')
    vert_index_dict = {}
    v_ind = 0
    for i in range(len(verts)):
        v = verts[i]
        val = binary[v[0], v[1]]
        if val == 255:
            vert_index_dict[i] = v_ind
            v_ind += 1
            continue
        assert (val == 0)
        vert_index_dict[i] = -1

    print('outputting verts')
    with open(crossed_vert_filename, 'w') as crossed_vert_file:
        for i in range(len(verts)):
            if vert_index_dict[i] == -1:
                continue
            v = verts[i]
            crossed_vert_file.write(str(v[0]) + ' ' + str(v[1]) + ' ' + v[2] + '\n')
        crossed_vert_file.close()

    print('outputting edges')
    with open(crossed_edge_filename, 'w') as crossed_edge_file:
        for e in edges:
            if vert_index_dict[e[0]] == -1 or vert_index_dict[e[1]] == -1:
                continue
            crossed_edge_file.write(str(vert_index_dict[e[0]]) + ' ' + str(vert_index_dict[e[1]]) + '\n')
        crossed_edge_file.close()


THREADS = 6
input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]
binary_dir = sys.argv[4]

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

pool = Pool(THREADS)
pool.map(function, image_filenames)
