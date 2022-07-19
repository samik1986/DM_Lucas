import sys
import csv
import os
from multiprocessing import Pool


def function(d):
    print('working on', d)
    coord_filename = os.path.join(d, 'coords.txt')
    with open(coord_filename, 'r') as coord_file:
        line = coord_file.readline()
        coord_file.close()
    shift = line.split(' ')
    nx = int(shift[0])
    ny = int(shift[1])
    nz = int(shift[2])

    vert_filename = os.path.join(d, 'vert.txt')
    verts = []
    with open(vert_filename, 'r') as vert_file:
        reader = csv.reader(vert_file, delimiter=' ')
        for row in reader:
            verts.append((int(row[0]), int(row[1]), int(row[2]), row[3]))
        vert_file.close()

    shifted = [(v[0] + nx, v[1] + ny, v[2] + nz, v[3]) for v in verts]
    output_filename = os.path.join(d, 'shifted-vert.txt')
    with open(output_filename, 'w') as output_file:
        for v in shifted:
            output_file.write(str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + ' ' + v[3] + '\n')
        output_file.close()


THREADS = 32
input_dir = sys.argv[1]


print(os.listdir(input_dir))

split_dirs = [os.path.join(input_dir, listing) + '/' for listing in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, listing))]
split_dirs.sort()

print('dirs:', len(split_dirs))

print('morse time')
pool = Pool(THREADS)
results = pool.map(function, split_dirs)
pool.close()
pool.join()

