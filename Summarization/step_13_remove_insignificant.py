import sys
import networkx as nx
import os
import csv
from multiprocessing import Pool
import matplotlib.image as mpimg
import numpy as np
import math
import matplotlib.pyplot as plt


def remove_deg2_nodes(graph):
    new_graph = graph
    count = 0
    for node in list(new_graph.nodes()):
        count += 1
        #print(count,'/',total)
        if new_graph.degree(node) == 2:
            edges = list(new_graph.edges(node))
            assert(len(edges) == 2)
            e0 = edges[0]
            e1 = edges[1]
            new_graph.add_edge(e0[1], e1[1])
            new_graph.remove_node(node)
    return new_graph


def line_function(val, cos, cap):
    capped_val = min(val, cap)
    return (ALPHA + cos) * capped_val


def compute_abs_cos_angle(v1, v2):
    v1_array = np.asarray(v1)
    v2_array = np.asarray(v2)

    if np.linalg.norm(v1_array) == 0 or np.linalg.norm(v2_array) == 0:
        return 0

    v1_unit = v1_array / np.linalg.norm(v1_array)
    v2_unit = v2_array / np.linalg.norm(v2_array)
    angle = np.arccos(np.dot(v1_unit, v2_unit))
    cos = math.cos(angle)

    #print(v1_array, v2_array, angle, cos)

    #sys.exit()

    return abs(cos)


def function(image_filename):
    print('working on', image_filename)
    image_output_dir = os.path.join(input_dir, os.path.splitext(image_filename)[0]) \
                       + '/' + ve_persistence_threshold + '_' + et_persistence_threshold + '/'
    vert_filename = os.path.join(image_output_dir, 'haircut-no-dup-vert.txt')
    paths_filename = os.path.join(image_output_dir, 'haircut-paths.txt')
    #sobel_filename = os.path.join(input_dir, os.path.splitext(image_filename)[0] + '/sobel-100.tif')
    output_edge_filename = os.path.join(image_output_dir, 'leaf-edge.txt')

    vector_filename = os.path.join(image_output_dir, '5_3_smooth-wpca.txt')

    print('reading verts')
    verts = []
    with open(vert_filename, 'r') as vert_file:
        reader = csv.reader(vert_file, delimiter=' ')
        for row in reader:
            verts.append([int(row[0]), int(row[1]), int(row[2])])
        vert_file.close()
    print(len(verts), 'verts', max([v[2] for v in verts]))

    print('reading paths')
    with open(paths_filename, 'r') as paths_file:
        content = paths_file.readlines()
        paths_file.close()

    paths = [c.strip().split(' ') for c in content]
    paths = [[int(n) for n in c] for c in paths]

    valid_paths = []
    for p in paths:
        '''
        vals = [verts[v][2] for v in p]
        if min(vals) < 50:
            continue
        '''
        valid_paths.append(p)

    degrees = {}
    for p in valid_paths:
        if p[0] not in degrees.keys():
            degrees[p[0]] = 1
        else:
            degrees[p[0]] += 1
        if p[len(p) - 1] not in degrees.keys():
            degrees[p[len(p) - 1]] = 1
        else:
            degrees[p[len(p) - 1]] += 1

    '''
    image = mpimg.imread(sobel_filename)
    image.astype('uint16')
    '''

    print('reading vectors')
    vectors = []
    with open(vector_filename, 'r') as vector_file:
        reader = csv.reader(vector_file, delimiter=' ')
        for row in reader:
            if float(row[1]) > 0:
                vectors.append([float(row[0]), float(row[1])])
            else:
                vectors.append([-float(row[0]), -float(row[1])])
        vector_file.close()

    print(len(verts), len(vectors))

    print('vector check:', min([abs(v[0]) for v in vectors]), max(abs(v[1]) for v in vectors))
    # sys.exit()

    '''
    plt.hist([v[0] for v in vectors], bins=20)
    plt.show()
    plt.clf()
    plt.hist([v[1] for v in vectors], bins=20)
    plt.show()
    plt.clf()
    '''

    vector_check_vert_filename = os.path.join(image_output_dir, 'vert-check.txt')
    vector_check_edge_filename = os.path.join(image_output_dir, 'edge-check.txt')
    FACTOR = 10
    print('factor:', FACTOR)

    with open(vector_check_vert_filename, 'w') as vcvf:
        for i in range(len(verts)):
            v = verts[i]
            vec = vectors[i]
            vcvf.write(str(v[0]) + ' ' + str(v[1]) + '\n')
            vcvf.write(str(v[0] + FACTOR * vec[0]) + ' ' + str(v[1] + FACTOR * vec[1]) + '\n')
        vcvf.close()

    with open(vector_check_edge_filename, 'w') as vcef:
        for i in range(len(verts)):
            vcef.write(str(2 * i) + ' ' + str(2 * i + 1) + '\n')
        vcef.close()

    with open(output_edge_filename, 'w') as output_edge_file:
        scores = []
        paths_to_consider = []
        for i in range(len(valid_paths)):
            #print('path:', i, '/', len(valid_paths))
            p = valid_paths[i]
            #print(p)
            if len(p) < 2:
                for j in range(len(p) - 1):
                    # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                    output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' 255\n')
                    #scores.append(255)
                '''
                output_edge_file.write(content[i] + ' 255\n')
                print('less than 2')
                '''
                continue

            first_degree = degrees[p[0]]
            second_degree = degrees[p[len(p) - 1]]

            '''
            if first_degree > 1 and second_degree > 1:
                for j in range(len(p) - 1):
                    # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                    output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' 255\n')
                    #scores.append(255)
                continue
            '''

            if first_degree == 1 and second_degree == 1:
                for j in range(len(p) - 1):
                    # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                    output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' 255\n')
                    #scores.append(255)

                '''
                output_edge_file.write(content[i] + ' 255\n')
                print('single path')
                '''
                continue

            assert(first_degree > 2 or second_degree > 2)
            # if False:
            if first_degree == 1 or second_degree == 1:
                if first_degree == 1:
                    p.reverse()

                # one more haircut
                if verts[p[0]][0] == verts[p[1]][0]:
                    direction = 1
                else:
                    assert (verts[p[0]][1] == verts[p[1]][1])
                    direction = 0
                dir_delta = 0
                for j in range(1, len(p)):
                    if verts[p[j - 1]][0] == verts[p[j]][0]:
                        current_direction = 1
                    else:
                        assert (verts[p[j - 1]][1] == verts[p[j]][1])
                        current_direction = 0
                    if current_direction == direction:
                        continue
                    direction = current_direction
                    dir_delta += 1
                if dir_delta <= 1:
                    continue

                func = [verts[k][2] for k in p]
                # print(func)

                keep = False
                max_val = max(func)
                current_min = func[0]
                for j in range(1, len(p)):
                    if func[j] > current_min + max_val * .05:
                        # print(func)
                        keep = True
                        break
                    current_min = min(current_min, func[j])

                delta = [0]
                for j in range(1, len(p)):
                    delta.append(func[j - 1] - func[j])

                if keep:
                    paths_to_consider.append(p)
                    '''
                    for j in range(len(p) - 1):
                        # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                        output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' 255\n')
                    '''
                    continue

                if not keep and sum(d > max_val * .95 for d in func) / len(p) > .75:
                    paths_to_consider.append(p)
                    '''
                    for j in range(len(p) - 1):
                        # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                        output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' 255\n')
                    '''
                    continue
            else:
                paths_to_consider.append(p)
                '''
                for j in range(len(p) - 1):
                    # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                    output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' 255\n')
                '''
                '''
                vals = []
                #cap = max([verts[vp][2] for vp in p]) / 2
                cap = 1
                for j in range(len(p)):
                    left = max(0, j - PATH_RADIUS)
                    right = min(len(p) - 1, j + PATH_RADIUS)

                    vl = verts[left]
                    vr = verts[right]

                    morse_vector = [vr[0] - vl[0], vr[1] - vl[1]]
                    true_vector = vectors[p[j]]
                    cos = compute_abs_cos_angle(morse_vector, true_vector)
                    if cos < 0:
                        print('cos', cos)
                        sys.exit()
                    func = min(float(verts[p[j]][2]), cap)
                    if func < 0:
                        print('func', func)
                        sys.exit()

                    val = line_function(func / cap, cos, 1)
                    if val < 0:
                        print('val', val)
                        sys.exit()
                    vals.append(val)

                integral = 0
                for j in range(len(vals) - 1):
                    integral += (vals[j] + vals[j+1]) / 2
                score = integral / (len(p) - 1)
                scores.append(score)

                for j in range(len(p) - 1):
                    # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                    output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' ' + str(int(255 * score)) + '\n')
            '''
            '''
            else:
                #assert(first_degree > 2 and second_degree > 2)
                # func = [verts[k][2] for k in p]
                # print(func)

                vals = []
                cos_list = []
                func_list = []
                #cap = max([verts[vp][2] for vp in p]) / 2
                cap = 255
                for j in range(len(p)):
                    left = max(0, j - PATH_RADIUS)
                    right = min(len(p) - 1, j + PATH_RADIUS)

                    vl = verts[left]
                    vr = verts[right]

                    morse_vector = [vr[0] - vl[0], vr[1] - vl[1]]
                    true_vector = vectors[p[j]]
                    cos = compute_abs_cos_angle(morse_vector, true_vector)
                    if cos < 0:
                        print('cos', cos)
                        sys.exit()
                    cos_list.append(cos)

                    func = min(float(verts[p[j]][2]), cap)
                    if func < 0:
                        print('func', func)
                        sys.exit()
                    func_list.append(func)

                    val = line_function(func / cap, cos, 1)
                    if val < 0:
                        print('val', val)
                        sys.exit()
                    vals.append(val)

                assert(len(p) == len(cos_list) == len(func_list) == len(vals))

                
                if min(cos_list) < .25:
                    continue
                

                
                integral = 0
                for j in range(len(vals) - 1):
                    integral += (vals[j] + vals[j + 1]) / 2
                score = integral / (len(p) - 1)
                
                #scores.append(sum(cos_list) / len(cos_list))
                score = sum(cos_list) / len(cos_list)
                #score = min(func_list) / max(func_list)
                #print(score)

                for j in range(len(p) - 1):
                    # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                    output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' ' + str(int(255 * score)) + '\n')
            '''

        for p in paths_to_consider:
            vals = []
            cos_list = []
            func_list = []
            # cap = max([verts[vp][2] for vp in p]) / 2
            cap = 255
            for j in range(len(p)):
                left = max(0, j - PATH_RADIUS)
                right = min(len(p) - 1, j + PATH_RADIUS)

                vl = verts[left]
                vr = verts[right]

                morse_vector = [vr[0] - vl[0], vr[1] - vl[1]]
                true_vector = vectors[p[j]]
                cos = compute_abs_cos_angle(morse_vector, true_vector)
                if cos < 0:
                    print('cos', cos)
                    sys.exit()
                cos_list.append(cos)

                func = min(float(verts[p[j]][2]), cap)
                if func < 0:
                    print('func', func)
                    sys.exit()
                func_list.append(func)

                val = line_function(func / cap, cos, 1)
                if val < 0:
                    print('val', val)
                    sys.exit()
                vals.append(val)

            assert (len(p) == len(cos_list) == len(func_list) == len(vals))

            '''
            if min(cos_list) < .25:
                continue
            '''

            integral = 0
            for j in range(len(vals) - 1):
                integral += (vals[j] + vals[j + 1]) / 2
            score = integral / (len(p) - 1)

            # scores.append(sum(cos_list) / len(cos_list))
            # score = sum(cos_list) / len(cos_list)
            # score = min(cos_list)
            score = sum(func_list) / len(func_list) / 255
            #print(func_list)
            # print(score)

            for j in range(len(p) - 1):
                # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' ' + str(int(255 * score)) + '\n')

            '''
            for j in range(len(p) - 1):
                # output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' 255\n')
            '''
        output_edge_file.close()


THREADS = 1
PATH_RADIUS = 3
input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]
MAX_INT = 255
ALPHA = 0

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

image_filenames = image_filenames[:1]

pool = Pool(THREADS)
pool.map(function, image_filenames)
