import sys
import csv
import os
import math

input_dir = sys.argv[1]
output_dir = sys.argv[2]
nx = int(sys.argv[3])
ny = int(sys.argv[4])
nz = int(sys.argv[5])

max_x = int(sys.argv[6])
max_y = int(sys.argv[7])
max_z = int(sys.argv[8])

overlap = int(sys.argv[9])

x_cubes = math.ceil(nx / max_x)
y_cubes = math.ceil(ny / max_y)
z_cubes = math.ceil(nz / max_z)

print('total cubes:', x_cubes * y_cubes * z_cubes)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

valid_dirs_filename = os.path.join(input_dir, 'valid-dirs.txt')

merged_valid_dirs_filename = os.path.join(output_dir, 'valid-dirs.txt')

print('reading valid dirs')
valid_dirs = set()
with open(valid_dirs_filename, 'r') as valid_dirs_file:
    reader = csv.reader(valid_dirs_file, delimiter=' ')
    for row in reader:
        #print(int(row[0]))
        valid_dirs.add(int(row[0]))
        #print('added')
    valid_dirs_file.close()
print('valid dirs:', len(valid_dirs))
#sys.exit()

with open(merged_valid_dirs_filename, 'w') as merged_valid_dirs_file:
    count = 0
    for k in range(0, z_cubes, 2):
        for j in range(0, y_cubes, 2):
            for i in range(0, x_cubes, 2):
                print('writing', count,'th config file')
                config_filename = os.path.join(output_dir, 'merge-config-' + str(count) + '.txt')

                cube_list = []
                start = k * x_cubes * y_cubes + j * y_cubes + i
                # 1
                cube_list.append([start, i, j, k, 1])
                if i + 1 != x_cubes:
                    # 2
                    cube_list.append([start + 1, i + 1, j, k, 2])
                if i + x_cubes < x_cubes * y_cubes:
                    # 3
                    cube_list.append([start + x_cubes, i, j + 1, k, 3])
                    if i + 1 != x_cubes:
                        # 4
                        cube_list.append([start + x_cubes + 1, i + 1, j + 1, k, 4])

                if i + x_cubes * y_cubes < x_cubes * y_cubes * z_cubes:
                    # 5
                    cube_list.append([start + x_cubes * y_cubes, i, j, k + 1, 5])

                    if i + 1 != x_cubes:
                        # 6
                        cube_list.append([start + x_cubes * y_cubes + 1, i + 1, j, k + 1, 6])

                    if i + x_cubes < x_cubes * y_cubes:
                        # 7
                        cube_list.append([start + x_cubes * y_cubes + x_cubes, i, j + 1, k + 1, 7])
                        if i + 1 != x_cubes:
                            # 8
                            cube_list.append([start + x_cubes * y_cubes + x_cubes + 1, i + 1, j + 1, k + 1, 8])

                valid = []

                with open(config_filename, 'w') as config_file:
                    config_file.write('merge-complex\n')
                    config_file.write(str(overlap) + ' ' + str(overlap) + ' ' + str(overlap) + '\n')

                    for cube in cube_list:
                        s = cube[0]
                        if s not in valid_dirs:
                            continue
                        valid.append(s)
                        tag = cube[4]
                        if tag == 1:
                            sx = cube[1] * max_x - overlap
                            sy = cube[2] * max_y - overlap
                            sz = cube[3] * max_z - overlap
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1
                        elif tag == 2:
                            sx = cube[1] * max_x
                            sy = cube[2] * max_y - overlap
                            sz = cube[3] * max_z - overlap
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1
                        elif tag == 3:
                            sx = cube[1] * max_x - overlap
                            sy = cube[2] * max_y
                            sz = cube[3] * max_z - overlap
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1
                        elif tag == 4:
                            sx = cube[1] * max_x
                            sy = cube[2] * max_y
                            sz = cube[3] * max_z - overlap
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1
                        elif tag == 5:
                            sx = cube[1] * max_x - overlap
                            sy = cube[2] * max_y - overlap
                            sz = cube[3] * max_z
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1
                        elif tag == 6:
                            sx = cube[1] * max_x
                            sy = cube[2] * max_y - overlap
                            sz = cube[3] * max_z
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1

                        elif tag == 7:
                            sx = cube[1] * max_x - overlap
                            sy = cube[2] * max_y
                            sz = cube[3] * max_z
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1

                        else:
                            assert(tag == 8)
                            sx = cube[1] * max_x
                            sy = cube[2] * max_y
                            sz = cube[3] * max_z
                            ex = sx + max_x + 2 * overlap - 1
                            ey = sy + max_y + 2 * overlap - 1
                            ez = sz + max_z + 2 * overlap - 1

                        config_file.write(
                            str(s) + ' ' + str(sx) + ' ' + str(sy) + ' ' + str(sz) + ' ' + str(ex) + ' ' + str(
                                ey) + ' ' + str(ez) + '\n')
                    config_file.close()

                if len(valid) > 0:
                    merged_valid_dirs_file.write(str(count) + '\n')

                count += 1
    merged_valid_dirs_file.close()
