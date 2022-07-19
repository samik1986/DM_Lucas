Discrete Morse Graph Reconstruction Code for Summarization and Skeletonization

Compiling C++ Code

Summarization:

dipha-2d-thresh/
mkdir build
cd build
cmake ../
make

dipha-output-2d-ve-et-thresh/
g++ ComputeGraphReconstruction.cpp

paths_src/
g++ ComputePaths.cpp

post-haircutpaths/
g++ ComputePaths.cpp

Skeletonzation:

dipha-3d/
mkdir build
cd build
cmake ../
make

SUMMARIZATION PIPELINE:

step_00_convert_jp2_to_tif.py
input_dir - sys.argv[1] - location of jp2 files
output_dir - sys.argv[2] - output dir location of tif files

step_01_split_tif_channels.py 
input_dir - sys.argv[1] - input dir of tif files (output_dir of step_00)
output_dir - sys.argv[2] - output dir location for single channel tifs.  This folder will have red/ and green/ subdirs.  NOTE: binary channels Samik has flipped (i.e. green binary channels correspond to red likelihood channels) for the sake of the viewer.  This matters in step 08.

step_02_crop_single_channel.py
input_dir - sys.argv[1] - input dir of single channel likelihood tif files (red/ or green/ dir from step_01)
output_dir - sys.argv[2] - output dir containing subfolder for each image. crop is done for runtime sake

step_03a_write_dipha.py
write dipha input file for each image
input_dir - sys.argv[1] - this should be the output_dir from step_02
Note that save_image_dir.m must be in cwd, make sure matlab path is correct

step_03b_write_vert.py
write vert file for each image
input_dir - sys.argv[1] - this should be the output_dir from step_02

step_04_run_dipha.py 
compute persistence for each image
input_dir - sys.argv[1] - this should be the output_dir from step_02
NOTE - make sure dipha path (dipha-2d-thresh/) is correct

step_05_run_matlab.py
convert persistence output to usable format for each image
input_dir - sys.argv[1] - this should be the output_dir from step_02

step_06_run_dimo_ve_et.py
run discrete morse graph reconstruction on each image
a folder is saved in each image subfolder ve_et - where ve and et are the 2 persistence threshold (ve negative critical edge, et positive critical edge)
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_07_shift_morse_verts.py
shift coordinates of morse output such that they are aligned with uncropped image.  this is needed for postprocessing with binary output and then posting to retsults to web
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_08_cross_morse_with_process.py
remove morse graph that does not lie in process detected region
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]
binary_dir - sys.argv[4] - this should be binary tif image folder from step_01.  If you are working with red channel data the binary segmentation output will be green channel.

step_09_remove_dup_edges.py
remove duplicate edges from Morse output (morse graph might have edges in overlapping v-paths, just cleaning up output for further downstream processing)
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_10_paths.py
get non-degree 2 paths of graph
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_11_haircut.py
remove "hairs" - branches coming off of fragments with at most one change in direction
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_12_post_haircut_paths.py
recalculate non degree 2 paths after haircut
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_13_remove_insignificant.py
remove paths that are "insignificant" - some sort of combo of intensity/vector alignment

step_14_align_morse_coords_with_webviewer.py
aligns coordinates with those of webviewer (currently assumes 24000 x 24000)
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_15_morse_to_geojson.py
converts morse graphs to geojson format for posting
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]

step_16_all_json_to_one_folder.py
input_dir - sys.argv[1] - this should be the output_dir from step_02
ve_persistence_threshold = sys.argv[2]
et_persistence_treshold = sys.argv[3]
output_dir = sys.argv[4] - output dir that will contain json for each image slice appropriateley named.  just need to move to appropriate directory to view on the web (PMD 1229: mitradevel.cshl.edu:/mnt/data001/dmdata/)


SKELETONIZATION PIPELINE:

step_00_split_3d_region.py
divide full brain image stack into easier to handle cubes
input_dir = sys.argv[1] - input image stack (crop masked tif!)
output_dir = sys.argv[2] - output_dir (contains a subfolder for each cube, as well as a file valid-dirs.txt that contains the list of cubes that were not masked out - only these cubes have directories)
x_len = int(sys.argv[3]) - cube length (pixels) for x axis
y_len = int(sys.argv[4]) - cube length (pixels) for y axis
z_len = int(sys.argv[5]) - cube length (pixels) for z axis
overlap = int(sys.argv[6]) - overlap in each axis for each cube

example: 128 128 128 16 -> first cube will be [0, 143] [0, 143], [0, 143]

step_01_write_dipha_input.py
generate dipha input file for each cube
input_dir = sys.argv[1] - output_dir from step 00
input_filename = sys.argv[2] - valid-dirs.txt file from step 00

step_02_run_dipha.py
compute persistence via dipha for each cube
input_dir = sys.argv[1] - output_dir from step 00
input_filename = sys.argv[2] - valid-dirs.txt file from step 00

step_03_convert_dipha_output.py
convert dipha output to usable file for each cube
input_dir = sys.argv[1] - output_dir from step 00
input_filename = sys.argv[2] - valid-dirs.txt file from step 00

step_04_shift_verts.py
shift the vertices to original coordinates not in cube
input_dir = sys.argv[1] - output_dir from step 00
input_filename = sys.argv[2] - valid-dirs.txt file from step 00

step_05_run_morse.py
run discrete morse graph reconstruction on each cube
input_dir = sys.argv[1] - output_dir from step 00
input_filename = sys.argv[2] - valid-dirs.txt file from step 00
persistence_threshold = int(sys.argv[3])

step_06_merge_config_gen.py
input_dir = sys.argv[1] - output_dir from step 00
input_filename = sys.argv[2] - valid-dirs.txt file from step 00
nx = int(sys.argv[3]) - x dim of original stack
ny = int(sys.argv[4]) - y dim of original stack
nz = int(sys.argv[5]) - z dim of original stack
max_x = int(sys.argv[6]) - x axis cube len
max_y = int(sys.argv[7]) - y axis cube len
max_z = int(sys.argv[8]) - z axis cube len
overlap = int(sys.argv[9]) - overlap between cubes

step_07_execute_merging.py
merge cubes together into larger cubes - number of cubes reduced by 8
raw_dir = sys.argv[1]
merge_dir = sys.argv[2]




