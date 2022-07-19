import numpy as np
import os
import sys
from matplotlib import image as mpimg

input_dir = sys.argv[1]
vert_filename = sys.argv[2]

image_filenames = [os.path.join(input_dir, l) for l in os.listdir(input_dir)]
image_filenames.sort()

nz = len(image_filenames)
image = mpimg.imread(input_dir + image_filenames[0])
nx, ny = image.shape
del image

print(nx, ny, nz)
# sys.exit()
im_cube = np.zeros([nx, ny, nz])

print('reading images')
i = 0
for name in image_filenames:
    sys.stdout.flush()
    # print(i, name)
    im_cube[:, :, i] = mpimg.imread(name)
    i = i + 1

print('writing images')
with open(vert_filename, 'w') as vert_file:
    for k in range(nz):
        sys.stdout.flush()
        #print('verts - working on image', k)
        for j in range(nx):
            for i in range(ny):
                vert_file.write(str(i) + ' ' + str(j) + ' ' + str(k) + ' ' + str(-im_cube[j, i, k]) + '\n')
    vert_file.close()
