from multiprocessing import Pool
import sys
import os
import matplotlib.image as mpimg


def function(cropped_dir):
    print('working on', cropped_dir)
    input_filename = os.path.join(cropped_dir, 'image.tif')
    dipha_output_filename = os.path.join(cropped_dir, 'dipha.input')
    diagram_filename = os.path.join(cropped_dir, 'diagram.bin')
    dipha_edge_filename = os.path.join(cropped_dir, 'dipha-thresh.edges')

    image = mpimg.imread(input_filename)
    nx, ny = image.shape

    command = 'mpiexec -n ' + str(
        MPI_THREADS) + ' ../../dipha-2d-original/build/dipha --upper_dim 2 ' + dipha_output_filename + ' ' + diagram_filename + ' ' + dipha_edge_filename + ' ' + str(
        nx) + ' ' + str(ny)
    # command = 'mpiexec -n 32 ../dipha/dipha-graph-recon/build/dipha --upper_dim 2 dipha/neuron1-smaller/complex.bin dipha/neuron1-smaller/persistence.diagram dipha/neuron1-smaller/dipha.edges 235 248 251'
    os.system(command)


MPI_THREADS = 1
THREADS = 6

input_dir = sys.argv[1]
cropped_image_dirs = [os.path.join(input_dir, listing) for listing in os.listdir(input_dir)]
cropped_image_dirs.sort()

pool = Pool(THREADS)
pool.map(function, cropped_image_dirs)
