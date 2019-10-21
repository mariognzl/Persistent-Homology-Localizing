"""An Example for the localization algorithm.
"""
import simpcells as sc
import homology as hom
import blowup as blp

# construct cells and cover:
a = sc.cell('a', [])
a.dimension = 0
b = sc.cell('b', [])
b.dimension = 0
c = sc.cell('c', [])
c.dimension = 0
d = sc.cell('d', [])
d.dimension = 0
e = sc.cell('e', [])
e.dimension = 0
f = sc.cell('f', [])
f.dimension = 0
cells0 = [a, b, c, d, e, f]

ab = sc.cell('ab', [a, b])
bc = sc.cell('bc', [b, c])
ad = sc.cell('ad', [a, d])
bd = sc.cell('bd', [b, d])
ce = sc.cell('ce', [c, e])
df = sc.cell('df', [d, f])
ef = sc.cell('ef', [e, f])
cells1 = [ab, bc, ad, bd, ce, df, ef]
for cell_iterator in cells1:
    cell_iterator.dimension = 1

abd = sc.cell('abd', [ab, ad, bd])
cells2 = [abd]
for cell_iterator in cells2:
    cell_iterator.dimension = 2

cell_list = cells0 + cells1 + cells2

part1 = [a, b, c, ab, bc]
part2 = [a, b, d, f, ab, ad, bd, df, abd]
part3 = [c, e, f, ce, ef]

# construct blowup:
new_cell_list = blp.construct_mv_blowup(cell_list, [part1, part2, part3])

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
