import sys
import networkx as nx
import os
import csv
from multiprocessing import Pool
import matplotlib.image as mpimg


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


def function(image_filename):
    print('working on', image_filename)
    image_output_dir = os.path.join(input_dir, os.path.splitext(image_filename)[0]) \
                       + '/' + ve_persistence_threshold + '_' + et_persistence_threshold + '/'
    vert_filename = os.path.join(image_output_dir, 'crossed-vert.txt')
    paths_filename = os.path.join(image_output_dir, 'paths.txt')
    #sobel_filename = os.path.join(input_dir, os.path.splitext(image_filename)[0] + '/sobel-100.tif')
    output_edge_filename = os.path.join(image_output_dir, 'haircut-edge.txt')
    print('reading verts')
    verts = []
    with open(vert_filename, 'r') as vert_file:
        reader = csv.reader(vert_file, delimiter=' ')
        for row in reader:
            verts.append([int(row[0]), int(row[1]), int(row[2])])
        vert_file.close()
    print(len(verts), 'verts')
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

    with open(output_edge_filename, 'w') as output_edge_file:
        for i in range(len(valid_paths)):
            #print('path:', i)
            p = valid_paths[i]
            #print(p)
            if len(p) < 2:
                output_edge_file.write(content[i] + '\n')
                print('less than 2')
                continue

            if verts[p[0]][0] == verts[p[1]][0]:
                direction = 1
            else:
                assert(verts[p[0]][1] == verts[p[1]][1])
                direction = 0
            delta = 0
            for j in range(1, len(p)):
                if verts[p[j-1]][0] == verts[p[j]][0]:
                    current_direction = 1
                else:
                    assert (verts[p[j-1]][1] == verts[p[j]][1])
                    current_direction = 0
                if current_direction == direction:
                    continue
                direction = current_direction
                delta += 1

            first_degree = degrees[p[0]]
            second_degree = degrees[p[len(p) - 1]]

            # haircut
            if delta <= 1 and (first_degree == 1 or second_degree == 1) and (first_degree > 2 or second_degree > 2):
                continue

            for j in range(len(p) - 1):
                output_edge_file.write(str(p[j]) + ' ' + str(p[j+1]) + '\n')
                # output_edge_file.write(str(p[j]) + ' ' + str(p[j + 1]) + ' ' + str(int(255 * min_func / max_func)) + '\n')
        output_edge_file.close()


THREADS = 6
input_dir = sys.argv[1]
ve_persistence_threshold = sys.argv[2]
et_persistence_threshold = sys.argv[3]

image_filenames = [listing for listing in os.listdir(input_dir)]
image_filenames.sort()

pool = Pool(THREADS)
pool.map(function, image_filenames)
