from multiprocessing import Pool
import sys
import os
import csv


input_dir = sys.argv[1]
input_filename = sys.argv[2]

os.system(
 "~/apps/MATLAB/R2021a/bin/matlab -nosplash -nodisplay -nodesktop -r \'parallel_dipha_input(\"" + input_dir + "\",\"" + input_filename + "\"); quit;\'")
