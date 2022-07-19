from multiprocessing import Pool
import sys
import os


def function(cropped_dir):
    print('working on', cropped_dir)
    dimo_input_filename = os.path.join(cropped_dir, 'dipha-edges.txt')
    vert_filename = os.path.join(cropped_dir, 'vert.txt')
    dimo_output_dir = os.path.join(cropped_dir, ve_persistence_threshold + '_' + et_persistence_treshold + '/')

    '''
    if os.path.exists(os.path.join(dimo_output_dir, 'dimo_edge.txt')):
        return
    '''
    if not os.path.exists(dimo_output_dir):
        os.mkdir(dimo_output_dir)

    morse_command = DM_PATH + ' ' + vert_filename + ' ' + dimo_input_filename + ' ' \
                    + str(ve_persistence_threshold) + ' ' + str(et_persistence_treshold) + ' ' + dimo_output_dir
    # print(morse_command)
    os.system(morse_command)


THREADS = 1
DM_PATH = './dipha-output-2d-ve-et-thresh/a.out'

input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

cropped_image_dirs = [os.path.join(input_dir, listing) for listing in os.listdir(input_dir)]
cropped_image_dirs.sort()

pool = Pool(THREADS)
pool.map(function, cropped_image_dirs)
