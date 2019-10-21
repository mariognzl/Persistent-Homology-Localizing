"""Compute barcodes for an easy example.
"""
import homology as hom
import simpcells as sc
import points_to_complex as ptc


# compute cells:
a = sc.cell('a', [])
b = sc.cell('b', [])
c = sc.cell('c', [])
d = sc.cell('d', [])

ab = sc.cell('ab', [a, b])
ac = sc.cell('ac', [a, c])
ad = sc.cell('ad', [a, d])
bd = sc.cell('bd', [b, d])
cd = sc.cell('cd', [c, d])

acd = sc.cell('acd', [ac, cd, ad])

# cell list:
K = [a, b, c, d, ab, ac, ad, bd, cd, acd]

# add order:
a.order = 0
b.order = 0
c.order = 0
d.order = 0

ac.order = 1
cd.order = 1

ab.order = 2

ad.order = 3
bd.order = 3

acd.order = 4

# add dimension:
a.dimension = 0
b.dimension = 0
c.dimension = 0
d.dimension = 0

ab.dimension = 1
ac.dimension = 1
ad.dimension = 1
bd.dimension = 1
cd.dimension = 1

acd.dimension = 2

# sort cell list by order:
K = ptc.sort_by_order(K)

# compute homology:
hom.compute_homology(K, step2=True)

# get barcodes:
homology_list, gen = hom.get_barcodes(K)
print(homology_list)

for k in K:
    print(k.order)
    print(k.name)
    print(k.basisel)
    print(k.partner)

# draw barcodes:
while True:
    number_dim = int(input('Which homology should be printed?'))
    hom.draw_barcode(homology_list, number_dim, K)
