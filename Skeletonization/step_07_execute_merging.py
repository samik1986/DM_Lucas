import sys
import csv
import os
from multiprocessing import Pool


def func(d):
    output_dir = os.path.join(merge_dir, str(d) + '/')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    complex_filename = os.path.join(output_dir, 'merge-complex.sc')
    if not os.path.exists(complex_filename):
        config_filename = os.path.join(merge_dir, 'merge-config-' + str(d) + '.txt')
        merge_command = MERGE_PATH + ' ' + raw_dir + ' ' + merge_dir + ' ' + config_filename + ' 64'
        os.system(merge_command)

    morse_dir = os.path.join(output_dir, '0/')
    if not os.path.exists(morse_dir):
        os.mkdir(morse_dir)
    morse_command = MORSE_PATH + ' ' + complex_filename + ' ' + morse_dir + ' 0 3'
    os.system(morse_command)


THREADS = 8
MERGE_PATH = './merger-hierarchical/a.out'
MORSE_PATH = './python/spt_cpp/spt_cpp'

raw_dir = sys.argv[1]
merge_dir = sys.argv[2]

merged_valid_dirs_filename = os.path.join(merge_dir, 'valid-dirs.txt')

valid = []
with open(merged_valid_dirs_filename, 'r') as mvdf:
    reader = csv.reader(mvdf, delimiter=' ')
    for row in reader:
        valid.append(int(row[0]))
    mvdf.close()

# valid = valid[:1]

pool = Pool(THREADS)
pool.map(func, valid)

