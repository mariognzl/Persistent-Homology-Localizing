"""Cech for evenly distributed points on a circle. Improved version without
   realization in real vector space.
"""
import tuple as tuple
import homology as hom
import simpcells as sc
import numpy as np
import points_to_complex as ptc
import time


# input number of points:
print('Compute homology for the Cech complex of evenly distributed points')
n = int(input('How many points?'))

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

list_of_cells = []
for t in list_of_tuples:
    # find boundary
    boundary_list_tuple = []
    for i in range(len(t.tuple)):
        boundary_list_tuple.append(tuple.tuple(t.tuple[:i] + t.tuple[i+1:]))
    boundary_list_cell = []
    for b in boundary_list_tuple:
        for d in list_of_cells:
            if d.name == b:
                boundary_list_cell.append(d)
    c = sc.cell(t, boundary_list_cell)
    list_of_cells.append(c)

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
        # check if all points are on one side
        i0 = len(t)-1
        i1 = 0
        check_one_side = False
        for i in range(len(t)-1):
            if t[i+1]-t[i] > n/2.0:
                check_one_side = True
                i0 = i
                i1 = i+1
                break
        if not check_one_side:
            if (t[0]-t[len(t)-1]) % n > n/2.0:
                check_one_side = True

        # all points on one side
        if check_one_side:
            # law of cosines: dist_cell^2 = R^2 + R^2 - 2R^2cos(phi)
            phi = ((t[i0]-t[i1]) % n)/float(n) * 2*np.pi
            dist_cell = np.sqrt(1+1-2*np.cos(phi))  # highest distance
            c.order = dist_cell/2.0

        # not all points on one side
        if not check_one_side:
            c.order = 1.0

print(time.time()-start)

# order cells:
print(' -- order cells -- ')
start = time.time()

list_of_cells = ptc.sort_by_order(list_of_cells)

print(time.time()-start)

# compute homology:
print(' -- compute homology -- ')
start = time.time()

hom.compute_homology(list_of_cells)

print(time.time()-start)

homology_list, gen = hom.get_barcodes(list_of_cells)

# print homolgoy
print('homology_list', homology_list)

# draw barcodes
while True:
    hom_number_to_display = int(input('Which homology should be printed?'))
    hom.draw_barcode(homology_list, hom_number_to_display, list_of_cells)#, max_value=1.1)
