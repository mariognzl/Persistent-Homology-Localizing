"""Set points in real vector space and compute its homology
"""

import homology as hom
import points_to_complex as ptc

'''pointlist'''
point_list = []
for i in range(1, 10):
    p1 = ptc.point([i, 0])
    p2 = ptc.point([i, 10])
    p3 = ptc.point([0, i])
    p4 = ptc.point([10, i])
    point_list.append(p1)
    point_list.append(p2)
    point_list.append(p3)
    point_list.append(p4)
point_list.append(ptc.point([0, 0]))
point_list.append(ptc.point([0, 10]))
point_list.append(ptc.point([10, 0]))
point_list.append(ptc.point([10, 10]))

point_list.append(ptc.point([5, 2]))
point_list.append(ptc.point([7, 2]))


max_radius = 1.3
hom_number_to_display = 1
cells = ptc.points_to_cells_VR(point_list, max_radius)

hom.compute_homology(cells)

barcodes, gen = hom.get_barcodes(cells)
hom.draw_barcode(barcodes, hom_number_to_display, cells)
