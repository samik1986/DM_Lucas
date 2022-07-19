from multiprocessing import Pool
import sys
import os
import csv


def function(cropped_dir):
    print('working on', cropped_dir)
    dimo_output_dir = os.path.join(cropped_dir, ve_persistence_threshold + '_' + et_persistence_threshold + '/')
    input_vert_filename = os.path.join(dimo_output_dir, 'dimo_vert.txt')
    output_vert_filename = os.path.join(dimo_output_dir, 'uncropped_dimo_vert.txt')
    crop_filename = os.path.join(cropped_dir, 'crop.txt')

    with open(crop_filename, 'r') as crop_file:
        reader = csv.reader(crop_file, delimiter=' ')
        for row in reader:
            x_add = int(row[0])
            y_add = int(row[2])
            break
        crop_file.close()

    with open(output_vert_filename, 'w') as output_vert_file:
        with open(input_vert_filename, 'r') as input_vert_file:
            reader = csv.reader(input_vert_file, delimiter=' ')
            for row in reader:
                # 2 is function value, need for vector
                output_vert_file.write(str(int(row[0]) + x_add) + ' ' + str(int(row[1]) + y_add) + ' ' + row[2] + '\n')
            input_vert_file.close()
        output_vert_file.close()


THREADS = 6
input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]

cropped_image_dirs = [os.path.join(input_dir, listing) for listing in os.listdir(input_dir)]
cropped_image_dirs.sort()

pool = Pool(THREADS)
pool.map(function, cropped_image_dirs)
