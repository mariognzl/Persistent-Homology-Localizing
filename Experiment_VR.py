"""Experiment to compute all barcodes for evenly distributed points for all
   dimensions.
   Note that all other python files need to be in the same folder.
"""
import Example_points_on_circle_VR_improved as bsp
import time


def simplify(homology_list):
    new_homology_list = []
    new_homology_list.append('\nhomology:')
    for h in homology_list:
        if len(h[1]) > 0:
            new_homology_list.append(h)
    return new_homology_list


def store(tuple, n):
    text = ''
    for t in tuple:
        text += str(t)+'\t'
    with open(str(n)+'.txt', "w+") as file:
        file.write(text)


def procedure(n):
    time_info = []
    info_tuple = []
    time_info.append('\ntime info:')

    start0 = time.time()  # here another ordering can be chosen:
    list_of_cells = bsp.VR_for_points_on_circle(n, ordering='points')
    end0 = time.time()

    info_tuple.append('number of cells:')
    info_tuple.append(len(list_of_cells))

    time_info.append('create cells:')
    time_info.append(str(end0-start0))

    distances = bsp.points_distance(n)
    info_tuple.append('distances:')
    info_tuple.extend(distances)

    start1 = time.time()
    homology_list = bsp.compute_homology(list_of_cells)
    end1 = time.time()
    time_info.append('compute homology:')
    time_info.append(str(end1-start1))

    simple_homology_list = simplify(homology_list)

    store_tuple = info_tuple + time_info + simple_homology_list
    print(store_tuple)
    store(store_tuple, n)


if __name__ == "__main__":
    n = int(input('Start with?'))
    m = int(input('End whith?'))
    while n <= m:
        procedure(n)
        n += 1
