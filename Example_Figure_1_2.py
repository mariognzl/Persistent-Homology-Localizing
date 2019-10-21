"""Set points in real vector space and compute its homology
"""

import homology as hom
import points_to_complex as ptc

'''pointlist'''
point_list = []

point_list.append(ptc.point([0, 0]))
point_list.append(ptc.point([2, 0]))
point_list.append(ptc.point([0, 1]))
point_list.append(ptc.point([2, 1]))


max_radius = 2
hom_number_to_display = 0
cells = ptc.points_to_cells_VR(point_list, max_radius)

hom.compute_homology(cells)

barcodes, gen = hom.get_barcodes(cells)
hom.draw_barcode(barcodes, hom_number_to_display, cells, max_value=max_radius)
