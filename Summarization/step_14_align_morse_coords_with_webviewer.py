from multiprocessing import Pool
import sys
import csv
import os


def function(image_filename):
    print('working on', image_filename)
    image_output_dir = os.path.join(input_dir, os.path.splitext(image_filename)[0]) \
                       + '/' + ve_persistence_threshold + '_' + et_persistence_threshold + '/'

    input_filename = os.path.join(image_output_dir, 'crossed-vert.txt')
    output_filename = os.path.join(image_output_dir, 'json-vert.txt')

    x_vals = []
    y_vals = []
    with open(output_filename, 'w') as output_file:
        with open(input_filename, 'r') as input_file:
            reader = csv.reader(input_file, delimiter=' ')
            for row in reader:
                raw_y = int(row[1])
                raw_x = int(row[0])

                x = raw_y
                y = - raw_x

                x_vals.append(x)
                y_vals.append(y)

                output_file.write(str(y) + ' ' + str(x) + ' 0 0' + '\n')
            input_file.close()
        output_file.close()


THREADS = 64
XSHIFT = 0
YSHIFT = 0
XRANGE = 24000
YRANGE = 24000

input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

pool = Pool(THREADS)
pool.map(function, image_filenames)
