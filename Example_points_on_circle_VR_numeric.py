"""Vietoris-Rips for evenly distributed points on a circle.
"""
import homology as hom
import points_to_complex as ptc
import numpy as np


def make_points_on_shpere(number_of_points):
    """Return a list of evenly distributed points on a circle."""
    list_of_points = []
    for i in range(number_of_points):
        new_point = ptc.point([np.cos(2*np.pi*i/number_of_points),
                               np.sin(2*np.pi*i/number_of_points)])
        list_of_points.append(new_point)
    return list_of_points


# create points:
number = int(input('How many points?'))
point_list = make_points_on_shpere(number)

print(point_list)
max_radius = 1.1

# create cells:
cells = ptc.points_to_cells_VR(point_list, max_radius)

# compute homology:
hom.compute_homology(cells)

# get barcodes
homology_list, gen = hom.get_barcodes(cells)
print('homology_list:', homology_list)
print(len(cells))

# draw barcodes
while True:
    hom_number_to_display = int(input('Which homology should be drawn?'))
    hom.draw_barcode(homology_list, hom_number_to_display, cells,
                     max_value=max_radius)
