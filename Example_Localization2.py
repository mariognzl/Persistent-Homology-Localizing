"""An Example for the localization algorithm.
"""
import simpcells as sc
import homology as hom
import blowup as blp

# construct cells and cover:
a = sc.cell('a', [])
b = sc.cell('b', [])
c = sc.cell('c', [])
d = sc.cell('d', [])
cells0 = [a, b, c, d]
for cell_iterator in cells0:
    cell_iterator.dimension = 0

ab = sc.cell('ab', [a, b])
ac = sc.cell('ac', [a, c])
ad = sc.cell('ad', [a, d])
bd = sc.cell('bd', [b, d])
cd = sc.cell('cd', [c, d])
cells1 = [ab, ac, ad, bd, cd]
for cell_iterator in cells1:
    cell_iterator.dimension = 1


cell_list = cells0 + cells1

part1 = [a, d, ad]
part2 = [a, b, c, d, ab, ac, bd, cd]

# construct blowup:
new_cell_list = blp.construct_mv_blowup(cell_list, [part1, part2])

# compute homology:
hom.compute_homology(new_cell_list, step2=True)  # with step 2
# hom.compute_homology(new_cell_list, step2=False)  # without step 2

# get barcodes:
homology_list, generator_list = hom.get_barcodes(new_cell_list)

# print homology list:
print(homology_list)

# print generator list:
for g in generator_list:
    print('\nhom', g[0])
    i = 0
    for f in g[1]:
        print('-Zelle', i)
        i = i+1
        for bas in f.basisel:
            cell_name = bas.name
            print(cell_name[0].name, cell_name[1])
