"""Vietoris-Rips for evenly distributed points on a circle. Improved version
   without realization in real vector space.
"""
import tuple as tuple
import homology as hom
import simpcells as sc
import numpy as np
import points_to_complex as ptc
import time


def VR_for_points_on_circle(n, ordering='distance'):
    """Compute Vietoris Rips complex for evenly distributed points on a circle.

    Args:
        n(int): Number of points.
        ordering(optional): The order for the simplicial cells is by default
            the radius of the corresponding Vietris-Rips complex. By setting
            ordering='points' the store the number of points between them.
            This gives a better representation for many points.
            Defaults to 'distance'.
        info(boolean, optional):

    Returns:
        list_of_cells(list): List of all cells representing the Vietoris-Rips
            complex.
        info_tuple(list): List with information
    """
    # create tuple for cells:
    print(' -- create list of all possible indices for cells -- ')
    start = time.time()  # time tracking

    list_of_tuples = []
    for i in range(1, n+1):
        for t in tuple.all_indices(i, n):
            list_of_tuples.append(tuple.tuple(t))

    print(time.time()-start)  # print time for this step

    # generate cells:
    print(' -- create cells and their boundary -- ')
    start = time.time()
    testind = 0  # index for number of iteration

    list_of_cells = []
    list_of_lists_of_cells = []  # improving speed
    for t in list_of_tuples:
        # find boundary
        boundary_list_tuple = []
        for i in range(len(t.tuple)):
            boundary_list_tuple.append(tuple.tuple(t.tuple[:i] + t.tuple[i+1:]))
        boundary_list_cell = []
        for b in boundary_list_tuple:
            if len(b.tuple) >= 1:
                for el in list_of_lists_of_cells[len(b.tuple)-1]:
                    if el.name == b:
                        boundary_list_cell.append(el)
        c = sc.cell(t, boundary_list_cell)
        list_of_cells.append(c)
        while len(t.tuple)-1 >= len(list_of_lists_of_cells):
            list_of_lists_of_cells.append([])
        list_of_lists_of_cells[len(t.tuple)-1].append(c)

        # print number to track the progress:
        if testind % 100 == 0:
            print(testind)
        testind += 1

    print(time.time()-start)
    print('number of cells:', len(list_of_cells))

    # add dimension
    print(' -- add dimension -- ')
    start = time.time()

    for c in list_of_cells:
        d = len(c.name.tuple) - 1
        c.dimension = d

    print(time.time()-start)

    # add order
    print(' -- add order -- ')
    start = time.time()

    for c in list_of_cells:
        t = c.name.tuple
        if len(t) == 1:
            c.order = 0.0
        else:
            # find points with the longest distance
            all_distances = []
            for i in t:
                for j in t:
                    all_distances.append(min([(i-j) % n, (j-i) % n]))
            maximum = max(all_distances)
            if ordering == 'distance':
                phi = (maximum)/float(n) * 2*np.pi
                dist_cell = np.sqrt(1+1-2*np.cos(phi))  # highest distance
                c.order = dist_cell/2  # order = radius
            if ordering == 'points':
                c.order = maximum  # order = difference of outer points

    print(time.time()-start)

    # order cells:
    print(' -- order cells -- ')
    start = time.time()

    list_of_cells = ptc.sort_by_order(list_of_cells)

    print(time.time()-start)

    return list_of_cells


def compute_homology(list_of_cells, max_val=None):
    """Compute the homology."""
    print(' -- compute homology -- ')
    start = time.time()

    hom.compute_homology(list_of_cells)

    print(time.time()-start)

    homology_list, gen = hom.get_barcodes(list_of_cells, max_value=max_val)

    # print homology
    print('homology_list', homology_list)
    return homology_list


def points_distance(n):
    """Distance of the points."""
    print('Abstaende der Punkte')
    distances = []
    for i in range(int(n/2.0+1.0)):
        phi = i/float(n) * 2*np.pi
        dist_cell = np.sqrt(1+1-2*np.cos(phi))  # highest distance
        print(i, ': ', dist_cell)
        distances.append(str(i)+': '+str(dist_cell))
    return distances


def draw_barcodes(homology_list, list_of_cells, max_val=None):
    """Draw barcodes."""
    while True:
        hom_number_to_display = int(input('Which homology should be printed?'))
        hom.draw_barcode(homology_list, hom_number_to_display, list_of_cells,
                         max_value=max_val)


if __name__ == "__main__":
    # input number of points:
    print('Compute homology for the Cech complex of evenly distributed points')
    n = int(input('How many points?'))

    list_of_cells = VR_for_points_on_circle(n)
    max_val = 1.0
    homology_list = compute_homology(list_of_cells)
    points_distance(n)
    draw_barcodes(homology_list, list_of_cells, max_val=max_val)
